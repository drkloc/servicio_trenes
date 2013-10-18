Package{
  ensure => present,
}

service{"iptables":
    ensure => stopped,
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
}

