import io
import time
import paramiko

source_filename = "/root/test/python3-10.tar"
dest_filename = "python3-10.tar"
ssh = paramiko.SSHClient()
ssh.load_system_host_keys(r"C:\Users\longh\.ssh\known_hosts")
ssh.connect(hostname="10.0.10.141", username="root")
source_sftp = ssh.open_sftp()
dest_transport = paramiko.Transport(("10.0.10.141", 2022))
dest_transport.connect(username="testuser", password="tiger")
dest_sftp = paramiko.SFTPClient.from_transport(dest_transport)


class GeneratorBytesIO(io.BytesIO):
    def __init__(self, generator):
        super().__init__()
        self.generator = generator

    def read(self, size=-1):
        if size == -1:
            return b"".join(self.generator)
        else:
            data = b""
            while len(data) < size:
                try:
                    chunk = next(self.generator)
                except StopIteration:
                    break
                data += chunk
            return data


def read_in_chunks(file_obj, chunk_size=1024 * 1024):
    while True:
        data = file_obj.read(chunk_size)
        if not data:
            break
        yield data


start = time.perf_counter()
source_file = source_sftp.open(source_filename)
iodata = GeneratorBytesIO(read_in_chunks(source_file))
res = dest_sftp.putfo(iodata, dest_filename)
source_file.close()
source_sftp.close()
dest_sftp.close()
dest_transport.close()
ssh.close()
end = time.perf_counter()
size = res.st_size
print('source:', '10.0.10.141')
print('destination:', '10.0.10.141 -P 2022')
print("chunk_size为：1024*1024")
print("传输文件为:", dest_filename)
print("数据量为：", size, '字节')
print("耗时：", end - start, 's')

