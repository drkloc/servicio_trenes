# http://nginx.org/packages/rhel/6/x86_64/RPMS/nginx-debug-1.4.3-1.el6.ngx.x86_64.rpm
class app($source, $ip, $redis, $mongo, $debug, $ssl){
  Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

  package{ 'python-devel': require => Package['epel-release-6-8.noarch']}

  package{ 'npm':
    require => Package['epel-release-6-8.noarch']
  }

  package {
    ['sqlite', 'git', 'curl', 'mercurial']:
      require => Package['python-devel']
  }

  package {'python-pip': require => Package['python-devel']}

  package { 
    ['fabric', 'virtualenv', 'virtualenvwrapper']:
      provider => 'pip',
      require  => Package['python-pip'],
  }
  
  package{
    ['libevent-devel', 'libevent-headers']:
      require => Package['epel-release-6-8.noarch']
  }

  firewall { '100 allow web access':
        port   => [80, 443],
        proto  => tcp,
        action => accept,
  }

  firewall { '100 allow zerorpc access':
        port   => [4242],
        proto  => tcp,
        action => accept,
  }

  firewall { '501 Allow all outbound traffic':
    chain      => 'OUTPUT',
    action     => 'accept',
    proto      => 'all',
  }

  file { "/opt/apps":
    ensure => "directory",
  }

  file { "/opt/apps/horariostrenes":
    ensure => "directory",
    require => File["/opt/apps"]
  }

  file { "/opt/apps/horariostrenes/static":
    ensure => "directory",
    require => File["/opt/apps/horariostrenes"],
  }

  file { "/opt/apps/horariostrenes/media":
    ensure => "directory",
    require => File["/opt/apps/horariostrenes"],
  }

  # User and app directories needed
  group {"horariostrenes":
    ensure => 'present',
    gid => 1000
  }

  user {"horariostrenes":
     gid => 'horariostrenes',
     comment => 'This user was created by Puppet',
     ensure => 'present',
     password => '$1$3BAQKf5y$cTtyoX5tKV.zrBdsI9rQE.',
     require => Group['horariostrenes'],
  }

  # Setup django app
  file { "/opt/apps/horariostrenes/django":
    recurse  => true,
    purge => true,
    force => true,
    source  => "$source/app/django",
    owner => 'horariostrenes',
    group => 'horariostrenes',
    require => [File["/opt/apps/horariostrenes"], User['horariostrenes']],
    ignore => ['.svn', '.hg', '.git', '*.pyc',  '.Python']
  }

  file { "/opt/apps/horariostrenes/django/servicetrenes/servicetrenes/settings_local.py":
    content => template('app/settings_local.py.erb'),
    require => File["/opt/apps/horariostrenes/django"]
  }

  file { "/opt/apps/horariostrenes/django/servicetrenes/servicetrenes/log/":
    ensure => "directory",
    require => File["/opt/apps/horariostrenes/django"]
  }

  exec { "fab DEV setup_virtualenv":
    cwd => '/opt/apps/horariostrenes/django/',
    require => File['/opt/apps/horariostrenes/django/servicetrenes/servicetrenes/settings_local.py'],
    logoutput => true,
  }

  exec { "fab DEV install_requirements":
    cwd => '/opt/apps/horariostrenes/django/',
    timeout => 0,
    require => Exec["fab DEV setup_virtualenv"],
    logoutput => true,
  }

  exec { "fab DEV setup_app":
    cwd => '/opt/apps/horariostrenes/django/',
    timeout => 0,
    require => Exec["fab DEV install_requirements"],
    logoutput => true,
  }

  # Setup node app
  file { "/opt/apps/horariostrenes/node":
    recurse  => true,
    purge => true,
    force => true,
    source  => "$source/app/node",
    owner => 'horariostrenes',
    group => 'horariostrenes',
    require => [File["/opt/apps/horariostrenes"], User['horariostrenes']],
    ignore => ['node_modules/*', 'node_modules']
  }

  exec { "npm install":
    cwd => '/opt/apps/horariostrenes/node/',
    timeout => 0,
    require => Package['npm'],
    logoutput => true,
    environment => 'HOME=/home/vagrant'
  }

  # Setup nginx
  package { 'nginx':
    provider => 'rpm',
    source => 'http://nginx.org/packages/rhel/6/x86_64/RPMS/nginx-1.4.3-1.el6.ngx.x86_64.rpm'
  }

  file { "/etc/nginx/nginx.conf":
    mode   => "0755",
    source => "puppet:///modules/app/nginx.conf",
    require => Package["nginx"],
    owner  => "root",
    group  => "root",
  }

  file { "/etc/nginx/conf.d/default.conf":
    mode   => "0755",
    content => template('app/default.conf.erb'),
    require => Package["nginx"],
    owner  => "root",
    group  => "root",
  }

  service { "nginx":
    ensure    => running,
    enable    => true,
    require   => [
      File["/etc/nginx/nginx.conf", "/etc/nginx/conf.d/default.conf"], 
    ],
  }

  # Setup supervisor to monitor django app, celeryd, celerybeat and node app
  package{ 'supervisor':}

  service { "supervisord":
    ensure    => running,
    enable    => true,
    require   => [
      Exec["fab DEV setup_app", "npm install"]
    ],
  }

  file { "/etc/supervisord.conf":
    mode   => "0755",
    content => template('app/supervisord.conf.erb'),
    require => Package["supervisor"],
    notify => Service["supervisord"],
    owner  => "root",
    group  => "root",
  }
}