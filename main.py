import requests
import concurrent.futures
import time

#input your discord token here to collect the lootbox
token = ''

ITEM_NAMES = {
    '1214340999644446724': 'Buster Blade',
    '1214340999644446723': 'Cute Plushie',
    '1214340999644446721': 'Wump Shell',
    '1214340999644446727': 'Speed Boost',
    '1214340999644446722': 'Secador',
    '1214340999644446725': 'Capacete',
    '1214340999644446720': 'Quack',
    '1214340999644446726': 'Banana',
    '1214340999644446728': 'Martelo'
}

def get_existing_quantities(data):
    existing_quantities = {ITEM_NAMES[item_id]: quantity for item_id, quantity in data['user_lootbox_data']['opened_items'].items() if item_id in ITEM_NAMES}
    return existing_quantities

TOTAL_ITEMS = {item_name: 0 for item_name in ITEM_NAMES.values()}

def send_request():
    headers = {
        'authorization': f'{token}',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIzLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI4MDkyOSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
    }

    response = requests.post('https://discord.com/api/v9/users/@me/lootboxes/open', headers=headers)
    data = response.json()
    update_collected_item(data)

def update_collected_item(data):
    existing_quantities = get_existing_quantities(data)
    opened_item_id = data['opened_item']
    opened_item_name = ITEM_NAMES.get(opened_item_id, 'Unknown Item')
    
    TOTAL_ITEMS[opened_item_name] = existing_quantities.get(opened_item_name, 0) + 1

    print(f"{opened_item_name}: {TOTAL_ITEMS[opened_item_name]}")

while True:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(send_request)
        executor.submit(send_request)

        time.sleep(3.3)