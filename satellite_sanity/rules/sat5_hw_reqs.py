#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_5']
name = 'Check basic HW requirements'

def os_arch(data):
  """
  Return architecture we are running on.
  """
  assert len(data['uname_m']) == 1
  return data['uname_m'][0]

def cpu_speed(data):
  """
  Return processor speed so we can ensure we have >=2.4GHz on x86_64.
  Returns None on s390x.
  """
  if os_arch(data) == 'x86_64':
    for line in data['proc_cpuinfo']:
      if line.startswith('cpu MHz'):
        val = line.split(':')[1].strip()
        return float(val)

def cpu_cache(data):
  """
  Return cache size so we can verify we have >=512KB on x86_64.
  Returns None on s390x.
  """
  if os_arch(data) == 'x86_64':
    for line in data['proc_cpuinfo']:
      if line.startswith('cache size'):
        val = line.split(':')[1].strip().replace(' KB', '')
        return float(val)

def ram_size(data):
  """
  Return RAM size so we can ensure wa have >=4GB of RAM.
  """
  for line in data['proc_meminfo']:
    if line.startswith('MemTotal:'):
      val = line.split(':')[1].strip().replace(' kB', '')
      return float(val)

def main(data):
  out = []
  var_arch = os_arch(data)
  var_cpu_speed = cpu_speed(data)
  exp_cpu_speed = 2400
  var_cpu_cache = cpu_cache(data)
  exp_cpu_cache = 512
  var_ram_size = ram_size(data)
  exp_ram_size = 1024 * 1024 * 4
  if var_arch == 'x86_64':
    if var_cpu_speed < exp_cpu_speed:
      out.append("CPU speed %s MHz is below minimal requirement of %s MHz" % (int(round(var_cpu_speed)), exp_cpu_speed))
    if var_cpu_cache < exp_cpu_cache:
      out.append("CPU cache %s KB is below minimal requirement of %s KB" % (int(round(var_cpu_cache)), exp_cpu_cache))
  if var_ram_size < exp_ram_size:
    out.append("RAM size %s kB is below minimal requirement of %s kB" % (var_ram_size, exp_ram_size))
  if out:
    return {'errors': out}

def text(result):
  out = ""
  out += "System runninng Satellite 5 should meet minimal required HW configuration:\n"
  for e in result['errors']:
    out += "  %s\n" % e
  out += "See https://access.redhat.com/documentation/en-US/Red_Hat_Satellite/5.7/html-single/Installation_Guide/index.html#x86_64_Hardware_Requirements\n"
  out += "See https://access.redhat.com/documentation/en-US/Red_Hat_Satellite/5.7/html-single/Installation_Guide/index.html#s390x_Hardware_Requirements"
  return out