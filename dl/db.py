"""
#
name
Q
Size
Last Try
Description
Time Added
Save To
Download Link
----------------------------
Status (online)
Time Left (online)
Transfer Rate (online)
-----------------------------
Download progress, chunks
lasthash
file hash

uuid
id::uuid::name::size::Lasttry:Descrition::TimeAdded::SaveTo::DonwloadLink::[Download Checklist]
"""
import os

from . import consts

record_order = ['uuid', 'filename', 'save_to', 'download_url', 'Q', 'size', 'last_try', 'description',
                'time_added', 'last_try_hash', 'file_hash', 'state_file', 'download_link']


# 'threads', 'block_size','limited_speed', 'download_block_count'
# 'download_link', 'download_chunk']


def add_item(metadata: dict):
    record = '::'.join([metadata[item] for item in record_order]) + '\n'
    with open(consts.MANAGER_DB_PATH, 'a') as db:
        db.write(record)
    return True


def delete_item(number: int):
    records = open(consts.MANAGER_DB_PATH).readlines()
    if len(records) > number:
        os.remove(records[number].split('::')[-1])
        return records.pop(number)


def update_item(number: int, metadata: dict):
    record = '::'.join([metadata[item] for item in record_order]) + '\n'
    records = open(consts.MANAGER_DB_PATH).readlines()
    if len(records) > number:
        records[number] = record


def fetch_item(number):
    result = {
        "#": number
    }
    record = open(consts.MANAGER_DB_PATH).readlines()[number]
    result.update({
        item: record[index] for index, item in enumerate(record_order)
    })
    return result


def fetch_all():
    result = dict()
    records = open(consts.MANAGER_DB_PATH).readlines()
    for number, record in enumerate(records):
        result.update({'#': number})
        result.update({
            item: record[index] for index, item in enumerate(record_order)
        })

    return result
