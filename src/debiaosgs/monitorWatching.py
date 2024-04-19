import requests
import json
import os
import sys
from teleBot import sendMsg
from loguru import logger
import galxeAPI as galxe
import datetime as dt


dir_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(dir_path, 'galxe.log')

logger.remove()
logger.add(log_path, format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
                              '<level>{level: ^7}</level> | '
                              '<level>{message}</level>')
logger.info('Starting.......')


# convert to abs path to avoid crontab error
space_list_path = 'space_list.txt'
campaign_list_path = 'result/campaign_list.json'
today = dt.date.today().strftime('%Y-%m-%d')
daily_campaign_path = f'result/daily_campaign_{today}.json'
dir_path = os.path.dirname(os.path.abspath(__file__))
space_list_file = os.path.join(dir_path, space_list_path)
campaign_list_file = os.path.join(dir_path, campaign_list_path)
daily_campaign_file = os.path.join(dir_path, daily_campaign_path)

debug_mode = False
if debug_mode == True:
    proxies = {
    'https': 'http://127.0.0.1:7890/',
    'http': 'http://127.0.0.1:7890/'
    }
else:
    proxies = None

def check_res(res):
    if 'errors' in res:
        message = "Failed to query " + space + ': ' + res['errors']
        if debug_mode == True:
            print(message)
        else:
            logger.error(message)
        return False
    else:
        return True

def read_campaign_file(campaign_file_path):
    if os.path.exists(campaign_file_path):
        with open(campaign_file_path, 'r') as file:
            result = json.load(file)
    else:
        result = {}
    return result


def main():
    # read space list
    with open(space_list_file, 'r', encoding='utf-8') as f:
        space_list = f.read().splitlines()
        space_list = [space.strip() for space in space_list if not (space=='' or space[0]=='#')]

    # read all campaigns
    old_space_dict = read_campaign_file(campaign_list_file)

    # read today's campaign list
    daily_campaign_dict = read_campaign_file(daily_campaign_file)

    # check each space
    new_space_dict = {}
    for space in space_list:
        try:
            if space not in old_space_dict.keys():
                old_campaign_list = []
            else:
                old_campaign_list = old_space_dict[space]
            new_space_dict[space] = old_campaign_list

            result = galxe.get_campaign_collections(space, proxies)
            if check_res(result):
                space_name = result['data']['space']['name']
                campaign_collection_id_list = [each['id'] for each in result['data']['space']['campaigns']['list']]
                for campaign_id in campaign_collection_id_list:
                    result = galxe.get_campaign_details(campaign_id, proxies)
                    if check_res(result):
                        if result['data']['campaign']['childrenCampaigns'] == None:
                            children_campaign_list = [result['data']['campaign']]
                        else:
                            children_campaign_list = result['data']['campaign']['childrenCampaigns']
                        old_campaign_id_list = [] if not old_campaign_list else [campaign['id'] for campaign in old_campaign_list]
                        daily_campaign_id_list = [] if not daily_campaign_dict else list(daily_campaign_dict.keys())
                        for campaign in children_campaign_list:
                            if (campaign['id'] not in old_campaign_id_list):
                                message = 'New task detected!\nSpace: %s\nLink: https://galxe.com/%s/campaign/%s' \
                                    % (space_name, space, campaign['id'])
                                new_space_dict[space].append({'id': campaign['id'], 'name': campaign['name']})
                                daily_campaign_dict[campaign['id']] = campaign['name']
                                if debug_mode == True:
                                    print(message + '\n')
                                else:
                                    sendMsg(message)
                            elif (campaign['recurringType'] == 'DAILY') and (campaign['id'] not in daily_campaign_id_list):
                                message = 'Daily task!\nSpace: %s\nLink: https://galxe.com/%s/campaign/%s' \
                                    % (space_name, space, campaign['id'])
                                daily_campaign_dict[campaign['id']] = campaign['name']
                                if debug_mode == True:
                                    print(message + '\n')
                                else:
                                    sendMsg(message)
        except Exception as e:
            logger.exception(e)
        finally:
            continue

    # update campaign list
    with open(campaign_list_file, 'w') as file:
        json.dump(new_space_dict, file)
    with open(daily_campaign_file, 'w') as file:
        json.dump(daily_campaign_dict, file)
    logger.info('success')


if __name__ == '__main__':
    main()
