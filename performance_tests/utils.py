import platform
import subprocess
import sys
import psutil
import json
import socket
import GPUtil

from datetime import datetime
from cpuinfo import get_cpu_info
from django import get_version as get_django_version
from django.conf import settings
from .models import TestResult


def get_full_system_info():
	info = {
		'system'    : get_os_info(),
		'python'    : get_python_info(),
		'packages'  : get_formatted_packages_list(),
		'django'    : get_django_info(),
		'cpu'       : get_processor_info(),
		'memory'    : get_memory_info(),
		'network'   : get_network_info(),
		'disks'     : get_disks_info(),
		'gpu'       : get_gpu_info(),
		'database'  : get_database_info(),
	}

	return info


def get_os_info():
	boot_time = datetime.fromtimestamp(psutil.boot_time())

	current_time = datetime.now()
	uptime = current_time - boot_time
	total_seconds = int( uptime.total_seconds() )

	days = total_seconds // (24 * 3600)
	hours = (total_seconds % (24 * 3600)) // 3600
	minutes = (total_seconds % 3600) // 60
	seconds = total_seconds % 60

	return {
		'os': platform.system(),
		'os_version': platform.release(),
		'os_details': platform.platform(),
		'architecture': platform.architecture()[0],
		'machine': platform.machine(),
		'hostname': platform.node(),
		'boot_time': boot_time,
		'uptime': f"{days} дней, {hours} часов, {minutes} минут, {seconds} секунд",
	}


def get_python_info():
	return {
		'version': platform.python_version(),
		'implementation': platform.python_implementation(),
		'compiler': platform.python_compiler(),
		'executable': sys.executable,
		'path': sys.path,
	}


def get_formatted_packages_list():
	try:
		# Получаем список пакетов в виде списка словарей
		packages_json = subprocess.check_output(
			[sys.executable, '-m', 'pip', 'list', '--format=json'],
			stderr = subprocess.DEVNULL
		).decode()

		packages = json.loads( packages_json )
		return sorted( packages, key = lambda x: x['name'].lower() )
	except:
		try:
			# Альтернативный метод, если json не поддерживается
			packages_raw = subprocess.check_output(
				[sys.executable, '-m', 'pip', 'list'],
				stderr = subprocess.DEVNULL
			).decode()
			return packages_raw
		except:
			return "Не удалось получить список пакетов"


def get_django_info():
	return {
		'version': get_django_version(),
		'debug': settings.DEBUG,
		'timezone': settings.TIME_ZONE,
		'installed_apps': settings.INSTALLED_APPS,
		'middleware': settings.MIDDLEWARE,
	}


def get_processor_info():
	cpu_info = get_cpu_info()
	return {
		'name': cpu_info['brand_raw'],
		'brand': _get_cpu_brand(),
		'cores': psutil.cpu_count(logical=False),
		'threads': psutil.cpu_count(logical=True),
		'usage': psutil.cpu_percent(interval=1),
		'usage_by_threads': psutil.cpu_percent(interval=1, percpu=True),
		'freq': psutil.cpu_freq().current if hasattr(psutil.cpu_freq(), 'current') else None,
	}


def _get_cpu_brand():
	try:
		if platform.system() == 'Windows':
			return platform.processor()

		elif platform.system() == 'Darwin':
			return subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string']).decode().strip()

		elif platform.system() == 'Linux':
			with open('/proc/cpuinfo') as f:
				for line in f:
					if line.strip() and line.split(':')[0].strip() == 'model name':
						return line.split(':')[1].strip()

		return platform.processor()
	except:
		return platform.processor()


def get_memory_info():
	return {
		'total'    : psutil.virtual_memory().total,
		'available': psutil.virtual_memory().available,
		'used'     : psutil.virtual_memory().used,
		'percent'  : psutil.virtual_memory().percent,
	}


def get_network_info():
	net_io = psutil.net_io_counters()

	return {
		'hostname'   : socket.gethostname(),
		'fqdn'       : socket.getfqdn(),
		'ip_address' : socket.gethostbyname( socket.gethostname() ),
		'io'         : net_io._asdict()
	}


def get_disks_info():
	disk_info = []

	for part in psutil.disk_partitions( all = True ):
		if part.fstype:
			try:
				usage = psutil.disk_usage( part.mountpoint )
				disk_info.append( {
					'device'    : part.device,
					'mountpoint': part.mountpoint,
					'fstype'    : part.fstype,
					'total'     : usage.total,
					'used'      : usage.used,
					'free'      : usage.free,
					'percent'   : usage.percent
				} )
			except:
				continue

	return disk_info


def get_database_info():
	return {
		'engine'            : settings.DATABASES['default']['ENGINE'],
		'name'              : settings.DATABASES['default']['NAME'],
		'test_records_count': TestResult.objects.count(),
	}


def get_gpu_info():
	gpu_info = []

	for gpu in GPUtil.getGPUs():
		if gpu:
			try:
				gpu_info.append( {
					'id'          : gpu.id,
					'name'        : gpu.name,
					'memory_free' : gpu.memoryFree,
					'memory_used' : gpu.memoryUsed,
					'memory_total': gpu.memoryTotal,
					'load'        : f"{gpu.load * 100:.1f}",
					'temperature' : gpu.temperature
				} )
			except:
				continue

	return gpu_info


def save_test_result( test_id, test_name, parameters, execution_time ):
	cpu_info = get_cpu_info()
	gpu_info = get_gpu_info()

	TestResult.objects.create(
		test_id        = test_id,
		test_name      = str( test_name ),
		parameters     = str( parameters ),
		execution_time = execution_time,

		python_version = f'{platform.python_implementation()} {platform.python_version()}',
		django_version = get_django_version(),

		os     = f'{platform.system()} {platform.release()}',
		cpu    = cpu_info['brand_raw'],
		memory = psutil.virtual_memory().total // (1024 * 1024),  # B -> MB
		gpu    = gpu_info[0]['name']
	)
