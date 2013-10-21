class mongodb($ip, $port=27017) {
    package {
        ['mongodb-server', 'mongodb']:
        require => Package['epel-release-6-8.noarch']
    }
    file { "/etc/mongodb.conf":
        mode    => "0644",
        content => template('mongodb/mongodb.conf.erb'),
        require => Package["mongodb", "mongodb-server"],
        owner   => "root",
        group   => "root",
    }
    firewall { '100 allow mongod access':
        port   => [$port],
        proto  => tcp,
        action => accept,
    }
    service { "mongod":
        require => File["/etc/mongodb.conf"],
        enable => true,
        ensure => running
    }
}