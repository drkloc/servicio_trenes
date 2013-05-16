exec { 'make_update':
    command => 'sudo yum update',
}

package {
  ['vim', 'git-core', 'curl']:
    ensure   => latest,
    require  => Exec['make_update'],
}

package {
  [
    'python-pip',
    'python-software-properties',
    'python-setuptools',
    'python27-devel',
    'build-essential'
  ]:
    ensure   => latest,
    require  => Exec['make_update'],
}

package{
  ['openssl-devel', 'gcc-c++']:
    ensure => latest,
    require => Exec['make_update']
}

package {
  ['fabric', 'virtualenv']:
    ensure   => latest,
    provider => pip,
    require  => Package[
      'python-devel',
      'python-pip',
      'python-setuptools'
    ],
}

package {
  ['redis', 'mongodb']:
    ensure => latest,
    require => Exec['make_update']
}

package{
  ['libevent', 'libevent-devel', 'libevent-headers']:
    ensure => lastest,
    require => Exec['make_update']
}