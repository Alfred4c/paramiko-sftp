import asyncssh
import asyncio
import time


async def copy_file(source, dest):
    async with asyncssh.connect('10.0.10.141', username='root') as source_conn:
        async with asyncssh.connect('10.0.10.141', port=2022, username='testuser', password='tiger') as dest_conn:
            async with source_conn.start_sftp_client() as source_sftp:
                async with dest_conn.start_sftp_client() as dest_sftp:
                    async with source_sftp.open(source, 'rb') as source_file:
                        source_stat = await source_sftp.stat(source)
                        file_size = source_stat.size
                        start_time = time.monotonic()
                        async with dest_sftp.open(dest, 'wb') as dest_file:
                            while True:
                                chunk = await source_file.read(4*1024*1024)
                                if  chunk:
                                    await dest_file.write(chunk)
                                if len(chunk) < 4*1024*1024:
                                    break
                        end_time = time.monotonic()
                        elapsed_time = end_time - start_time
                        print(
                            f"File Name:go1.20.2.linux-amd64.tar.gz\n"
                            f"Size: {file_size} bytes. Time elapsed: {elapsed_time} seconds\n"
                            f". Chunk size: 4M bytes.")


async def main():
    await copy_file('/root/test/go1.20.2.linux-amd64.tar.gz', 'go1.20.2.linux-amd64.tar.gz')


if __name__ == '__main__':
    asyncio.run(main())
