import asyncio
import random
from urllib.parse import unquote, quote

import aiohttp
import json
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw import types
from .agents import generate_random_user_agent
from bot.config import settings

from bot.utils import logger
from bot.exceptions import InvalidSession
from .headers import headers


class Tapper:
    def __init__(self, tg_client: Client):
        self.session_name = tg_client.name
        self.tg_client = tg_client
        self.user_id = 0
        self.username = None
        self.first_name = None
        self.last_name = None
        self.fullname = None
        self.start_param = None

        self.session_ug_dict = self.load_user_agents() or []

        headers['User-Agent'] = self.check_user_agent()

    async def generate_random_user_agent(self):
        return generate_random_user_agent(device_type='android', browser_type='chrome')

    def save_user_agent(self):
        user_agents_file_name = "user_agents.json"

        if not any(session['session_name'] == self.session_name for session in self.session_ug_dict):
            user_agent_str = generate_random_user_agent()

            self.session_ug_dict.append({
                'session_name': self.session_name,
                'user_agent': user_agent_str})

            with open(user_agents_file_name, 'w') as user_agents:
                json.dump(self.session_ug_dict, user_agents, indent=4)

            logger.success(f"<light-yellow>{self.session_name}</light-yellow> | User agent saved successfully")

            return user_agent_str

    def load_user_agents(self):
        user_agents_file_name = "user_agents.json"

        try:
            with open(user_agents_file_name, 'r') as user_agents:
                session_data = json.load(user_agents)
                if isinstance(session_data, list):
                    return session_data

        except FileNotFoundError:
            logger.warning("User agents file not found, creating...")

        except json.JSONDecodeError:
            logger.warning("User agents file is empty or corrupted.")

        return []

    def check_user_agent(self):
        load = next(
            (session['user_agent'] for session in self.session_ug_dict if session['session_name'] == self.session_name),
            None)

        if load is None:
            return self.save_user_agent()

        return load

    def info(self, message):
        from bot.utils import info
        info(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def debug(self, message):
        from bot.utils import debug
        debug(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def warning(self, message):
        from bot.utils import warning
        warning(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def error(self, message):
        from bot.utils import error
        error(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def critical(self, message):
        from bot.utils import critical
        critical(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    def success(self, message):
        from bot.utils import success
        success(f"<light-yellow>{self.session_name}</light-yellow> | {message}")

    async def get_tg_web_data(self, proxy: str | None) -> str:
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            with_tg = True

            if not self.tg_client.is_connected:
                with_tg = False
                try:
                    await self.tg_client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            while True:
                try:
                    peer = await self.tg_client.resolve_peer('catsgang_bot')
                    break
                except FloodWait as fl:
                    fls = fl.value

                    logger.warning(f"<light-yellow>{self.session_name}</light-yellow> | FloodWait {fl}")
                    logger.info(f"<light-yellow>{self.session_name}</light-yellow> | Sleep {fls}s")

                    await asyncio.sleep(fls + 3)

            if settings.REF_ID == '':
                self.start_param = 'eVMDZF6Fxdb8eNnjocoOP'
            else:
                self.start_param = settings.REF_ID
            InputBotApp = types.InputBotAppShortName(bot_id=peer, short_name="join")

            web_view = await self.tg_client.invoke(RequestAppWebView(
                peer=peer,
                app=InputBotApp,
                platform='android',
                write_allowed=True,
                start_param=self.start_param
            ))

            auth_url = web_view.url
            tg_web_data = unquote(
                string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0])

            try:
                information = await self.tg_client.get_me()
                self.user_id = information.id
                self.first_name = information.first_name or ''
                self.last_name = information.last_name or ''
                self.username = information.username or ''
            except Exception as e:
                print(e)

            if with_tg is False:
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(
                f"<light-yellow>{self.session_name}</light-yellow> | Unknown error during Authorization: {error}")
            await asyncio.sleep(delay=3)

    async def create_user(self, http_client: aiohttp.ClientSession):
        try:
            response = await http_client.post(url=f'https://cats-backend-cxblew-prod.up.railway.app/user/create?'
                                                  f'referral_code={self.start_param}')
            if response.status in [200, 201]:
                self.success('Successfully created user')
            else:
                return

        except Exception as e:
            self.error(f"Error in create user {e}")

    async def get_user_info(self, http_client: aiohttp.ClientSession):
        try:
            response = await http_client.get(url='https://cats-backend-cxblew-prod.up.railway.app/user')
            resp_json = await response.json()
            ref_rewards = resp_json.get('referrerReward')
            tasks_rewards = resp_json.get('tasksReward')
            age = resp_json.get('telegramAge')
            age_reward = resp_json.get('telegramAgeReward')
            total_rewards = resp_json.get('totalRewards')
            self.info(f"<lc>Telegram age: {age} year</lc> <lr>|</lr> <lg>Total balance: {total_rewards}, "
                      f"where {ref_rewards} from referrals, {tasks_rewards} from tasks and {age_reward} from account "
                      f"age</lg>")
        except Exception as e:
            self.error(f"Error in get user info {e}")

    async def get_tasks(self, http_client: aiohttp.ClientSession):
        try:
            response = await http_client.get(url='https://cats-backend-cxblew-prod.up.railway.app/'
                                                 'tasks/user?group=cats')
            resp_json = await response.json()
            return resp_json
        except Exception as e:
            self.error(f"Error in get tasks {e}")

    async def do_openlink_tasks(self, http_client: aiohttp.ClientSession, tasks):
        try:
            all_tasks = tasks['tasks']
            open_link_ids = [(task['id'], task['rewardPoints']) for task in all_tasks if task['type'] == 'OPEN_LINK' and task['completed']
                             is False]
            if open_link_ids:
                for id, reward in open_link_ids:
                    response = await http_client.post(
                        url=f"https://cats-backend-cxblew-prod.up.railway.app/tasks/{id}/complete",
                        json={})
                    resp_json = await response.json()
                    if resp_json.get('success') is True:
                        self.success(f"Done open link task with id - {id}, got - <lc>{reward} points</lc>")
        except Exception as e:
            self.error(f"Error in parse openlink tasks {e}")

    async def do_joinchannel_tasks(self, http_client: aiohttp.ClientSession, tasks):
        try:
            all_tasks = tasks['tasks']
            channel_task_ids_with_urls = [(task['id'], task['params']['channelUrl'], task['rewardPoints']) for task in all_tasks if
                                          task['type'] == 'SUBSCRIBE_TO_CHANNEL' and task['completed'] is False]
            if channel_task_ids_with_urls:
                for id, url, reward in channel_task_ids_with_urls:
                    username = url.split('https://t.me/')[1]
                    if not self.tg_client.is_connected:
                        await self.tg_client.connect()

                    await self.tg_client.join_chat(username)
                    await asyncio.sleep(1)
                    response = await http_client.post(url=f'https://cats-backend-cxblew-prod.up.railway.app/'
                                                          f'tasks/{id}/check', json={})
                    resp_json = await response.json()
                    if resp_json.get('completed') is True:
                        self.success(f'Done join channel task with id - {id}, got - <lc>{reward} points</lc>')

                    await self.tg_client.leave_chat(username)

                    if self.tg_client.is_connected:
                        await self.tg_client.disconnect()
        except Exception as e:
            self.error(f"Error in join channel tasks {e}")

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info(f"<light-yellow>{self.session_name}</light-yellow> | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"<light-yellow>{self.session_name}</light-yellow> | Proxy: {proxy} | Error: {error}")

    async def run(self, proxy: str | None) -> None:
        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        http_client = CloudflareScraper(headers=headers, connector=proxy_conn)

        if proxy:
            await self.check_proxy(http_client=http_client, proxy=proxy)

        tg_web_data = await self.get_tg_web_data(proxy=proxy)
        http_client.headers['Authorization'] = f'tma {tg_web_data}'

        while True:
            try:
                await self.create_user(http_client)
                await self.get_user_info(http_client)

                tasks = await self.get_tasks(http_client)
                if tasks:
                    await self.do_openlink_tasks(http_client, tasks)
                    if settings.DO_CHANNELS_TASKS:
                        await self.do_joinchannel_tasks(http_client, tasks)
                else:
                    continue

                logger.info(f"<light-yellow>{self.session_name}</light-yellow> | <lr>Thanks for using HiddenCode bot, now "
                            f"you can close bot, because there is no more functions that we can interact</lr>")

                await asyncio.sleep(36000)

            except InvalidSession as error:
                raise error

            except Exception as error:
                logger.error(f"<light-yellow>{self.session_name}</light-yellow> | Unknown error: {error}")
                await asyncio.sleep(delay=3)


async def run_tapper(tg_client: Client, proxy: str | None):
    try:
        await Tapper(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
