Package{
  ensure => present,
}

service{"iptables":
    ensure => stopped,
}

# package { 'epel-release-6-8.noarch':
#   provider => 'rpm',
#   source => 'http://epel.mirror.mendoza-conicet.gob.ar/6/x86_64/epel-release-6-8.noarch.rpm',
#   ensure => present
# }

# package{
#   ['libevent-devel', 'libevent-headers']:
# }

# class systools{
#   package {
#     ['curl', 'wget']:
#       require => Package['epel-release-6-8.noarch']
#   }
# }

# class python{
#   package{
#     ['python-devel']:
#       require => Package['epel-release-6-8.noarch'],
#   }

#   package {
#     [
#       'python-pip',
#       'python-setuptools',
#     ]:
#       require => Package['python-devel']
#   }
#   package {
#     ['fabric', 'virtualenv']:
#       provider => 'pip',
#       require  => Package[
#         'python-devel',
#         'python-pip',
#         'python-setuptools'
#       ],
#   }
# }

# class nodejs{
#   package{
#     ['nodejs', 'npm']:
#       require => Package['epel-release-6-8.noarch'],
#   }
# }

# class mongodb{
#   package {
#     ['mongodb-server', 'mongodb']:
#       require => Package['epel-release-6-8.noarch']
#   }
#   service { "mongod":
#     enable => true,
#     ensure => running
#   }
# }

include redis
include django_app
