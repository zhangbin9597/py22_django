from fdfs_client.client import Fdfs_client

if __name__ == '__main__':
    client = Fdfs_client('client.conf')
    ret = client.upload_by_filename('/home/python/Desktop/1.jpg')
    print(ret)
    '''
    {
        'Remote file_id': 'group1/M00/00/00/wKh8gFzOuuqAam1eAABCJh-yXAg048.jpg',
        'Group name': 'group1',
        'Local file name': '/home/python/Desktop/1.jpg',
        'Storage IP': '192.168.124.128',
        'Status': 'Upload successed.',
        'Uploaded size': '8.00KB'
    }
    '''
