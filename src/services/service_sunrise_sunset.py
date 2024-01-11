# -*- coding: utf-8 -*-

import aiohttp
import traceback
from datetime import datetime, timedelta
from pydantic import ValidationError
from schemas.schema_sunrise_sunset import (
    InputSunriseSunsetSchema,
    ExternalSubmmitSunriseSunsetSchema,
    ExternalResponseSunriseSunsetSchema,
    OutputSunriseSunsetSchema)

class SunriseSunsetApi(object):
    def __init__(self, inputed_params: InputSunriseSunsetSchema) -> None:
        self.inputed_params = inputed_params
        self.url_api = 'https://api.sunrise-sunset.org/json'

    async def seconds_to_hhmmss(self, total_seconds):
        """ get hour to format HH:MM:SS from total seconds """
        hours, remainder = divmod(total_seconds, 3600)
        minutes, total_seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{total_seconds:.6f}".split('.')[0]

    async def get_remaing_time(
        self,
        request_datetime: datetime,
        exact_time: datetime,
        session: aiohttp.ClientSession,
        external_params: dict) -> datetime or None:
        """ Get remaing time to event sunrise or sunset """
        try:
            if exact_time >= request_datetime:
                exact_time_to_24h = exact_time.strftime('%d-%m-%Y %H:%M:%S')
                return (exact_time - request_datetime, exact_time_to_24h)
            else:
                date = (request_datetime + timedelta(days=1))
                sended_params = {
                    'lat': self.inputed_params.latitude,
                    'lng': self.inputed_params.longitude,
                    'date': date.strftime('%Y-%m-%d')}
                external_params = ExternalSubmmitSunriseSunsetSchema(**sended_params).dict(exclude_none=True)
                async with session.get(self.url_api, params=external_params, timeout=60) as resp:
                    if resp.status != 200:
                        return None
                    else:
                        resp_json = await resp.json()
                        validated_output_external_api = ExternalResponseSunriseSunsetSchema(**resp_json)
                        if self.inputed_params.type == 'sunrise':
                            exact_time_str_12hr_to_sunrise = datetime.strptime(
                                f'{date.day}-{date.month}-{date.year} ' + \
                                validated_output_external_api.results.get('sunrise'), '%d-%m-%Y %I:%M:%S %p')
                            exact_time_str_24hr_to_sunrise = exact_time_str_12hr_to_sunrise.strftime(
                                '%d-%m-%Y %H:%M:%S')
                            return (exact_time_str_12hr_to_sunrise - request_datetime, exact_time_str_24hr_to_sunrise)
                        else:
                            exact_time_str_12hr_to_sunset = datetime.strptime(
                                f'{date.day}-{date.month}-{date.year} ' + \
                                validated_output_external_api.results.get('sunset'), '%d-%m-%Y %I:%M:%S %p')
                            exact_time_str_24hr_to_sunset = exact_time_str_12hr_to_sunset.strftime(
                                '%d-%m-%Y %H:%M:%S')
                            return (exact_time_str_12hr_to_sunset - request_datetime, exact_time_str_24hr_to_sunset)
        except ValidationError:
            traceback.print_exc()
            return (None, None)
        except Exception:
            traceback.print_exc()
            return (None, None)

    async def get_external_data(self) -> tuple:
        """ GET request to https://api.sunrise-sunset.org/json """
        try:
            sended_params = {
                'lat': self.inputed_params.latitude,
                'lng': self.inputed_params.longitude}
            external_params = ExternalSubmmitSunriseSunsetSchema(**sended_params).dict(exclude_none=True)
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url_api, params=external_params, timeout=60) as resp:
                    if resp.status != 200:
                        return (resp.status, await resp.json())
                    else:
                        resp_json = await resp.json()
                        request_datetime = datetime.now()
                        validated_output_external_api = ExternalResponseSunriseSunsetSchema(**resp_json)
                        exact_time_str_12hr_to_sunrise = datetime.strptime(
                            f'{request_datetime.day}-{request_datetime.month}-{request_datetime.year} ' + \
                            validated_output_external_api.results.get('sunrise'), '%d-%m-%Y %I:%M:%S %p')
                        remaing_time_to_sunrise, exact_time_str_24hr_to_sunrise = await self.get_remaing_time(
                            request_datetime=request_datetime,
                            exact_time=exact_time_str_12hr_to_sunrise,
                            session=session,
                            external_params=external_params)
                        exact_time_str_12hr_to_sunset = datetime.strptime(
                            f'{request_datetime.day}-{request_datetime.month}-{request_datetime.year} ' + \
                            validated_output_external_api.results.get('sunset'), '%d-%m-%Y %I:%M:%S %p')
                        remaing_time_to_sunset, exact_time_str_24hr_to_sunset = await self.get_remaing_time(
                            request_datetime=request_datetime,
                            exact_time=exact_time_str_12hr_to_sunset,
                            session=session,
                            external_params=external_params)
                        internal_output = {
                            'remaing_time':
                                await self.seconds_to_hhmmss(total_seconds=remaing_time_to_sunrise.total_seconds())
                                if self.inputed_params.type == 'sunrise' \
                                else await self.seconds_to_hhmmss(total_seconds=remaing_time_to_sunset.total_seconds()),
                            'exact_datetime':
                                exact_time_str_24hr_to_sunrise  \
                                if self.inputed_params.type == 'sunrise' \
                                else exact_time_str_24hr_to_sunset,
                            'request_datetime': request_datetime.strftime('%d-%m-%Y %H:%M:%S')}
                        validated_output_internal_api = OutputSunriseSunsetSchema(**internal_output)
                        response = {
                            'inputs': {
                                'type': self.inputed_params.type,
                                'latitude': self.inputed_params.latitude,
                                'longitude': self.inputed_params.longitude
                            },
                            'output': validated_output_internal_api.model_dump()}
                        return (200, response)
        except ValidationError as e:
            traceback.print_exc()
            return (422, str(e.errors()))
        except Exception:
            traceback.print_exc()
            return (502, '502 - Bad Gateway')
