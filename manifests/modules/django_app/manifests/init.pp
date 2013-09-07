class django_app{
  package{
    ['httpd', 'mod_wsgi']:
  }

  file { "/opt/apps/trenes/static":
    ensure => "directory",
  }
  file { "/opt/apps/trenes/app.wsgi":
    mode => "0644",
    source  => "puppet:///modules/django_app/app.wsgi",
    owner => "root",
    group => "root"
  }

  file { "/etc/httpd/conf.d/vhost.conf":
    mode    => "0644",
    source  => "puppet:///modules/django_app/vhost.conf",
    require => [
      Package["httpd","mod_wsgi"],
      File["/opt/apps/trenes/static"],
      File["/opt/apps/trenes/app.wsgi"]
    ], 
    owner   => "root",
    group   => "root",
  }
  
  service { "httpd":
    enable => true,
    ensure => running,
    require => File["/etc/httpd/conf.d/vhost.conf"]
  }

}