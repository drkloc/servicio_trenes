Package{
  ensure => present,
}

package { 'epel-release-6-8.noarch':
    provider => 'rpm',
    source => 'http://download-i2.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm',
}

class {'redis':
	ip => '127.0.0.1',
}

class {'mongodb':
	ip => '127.0.0.1',
}

class {'app':
	source => $source,
	ip => $ip,
	redis => '127.0.0.1:6379',
	mongo => 'horariostrenes:127.0.0.1:27017',
	debug => $debug,
	ssl => 'false',
	require => Class['redis', 'mongodb']
}

