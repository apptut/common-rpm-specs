Name:           php
Version:        7.3.2
Release:        3%{?dist}
Summary:        Php%{version} rpm package

License:        AGPLv3 
URL:		http://php.net/ChangeLog-7.php#%{version}
Source0:        http://cn.php.net/distributions/%{name}-%{version}.tar.gz
Source1:        php.ini

BuildRequires:  libxml2-devel,gcc,make,openssl-devel,zlib-devel,pcre-devel,libcurl-devel >= 7.15.5

Requires:	zip, unzip


%description
基于php7官方版本制作的rpm包，该包未编译GD库，如有需要请自行安装扩展库。

%package devel
Group: Development/Libraries
Summary: Development php package

Requires: autoconf

%description devel
Development files for php

%prep
%setup -q


%build
%configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
    	--sbindir=%{_sbindir} \
    	--sysconfdir=%{_sysconfdir}/php \
	--with-libdir=%{_lib} \
    	--with-config-file-path=%{_sysconfdir}/php \
	--libdir=%{_libdir}/php \
	--mandir=%{_mandir} \
	--datadir=%{_datadir} \
    	--includedir=%{_includedir} \
	--localstatedir=%{_localstatedir} \
	--enable-fpm \
	--enable-mbstring \
	--enable-calendar \
       	--with-pdo-mysql \
	--without-sqlite3 \
	--without-pdo-sqlite \
	--with-openssl \
	--with-zlib \
	--with-curl \
	--disable-phpdbg 

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/php/php-fpm.d

install -d $RPM_BUILD_ROOT%{_unitdir}

install -m0644 sapi/fpm/php-fpm.service $RPM_BUILD_ROOT%{_unitdir}/php-fpm.service
install -m0644 sapi/fpm/www.conf $RPM_BUILD_ROOT%{_sysconfdir}/php/php-fpm.d/
install -m0644 sapi/fpm/php-fpm.conf $RPM_BUILD_ROOT%{_sysconfdir}/php/php-fpm.conf
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/php/php.ini

make INSTALL_ROOT=$RPM_BUILD_ROOT install

# 删除make install 安装的多余文件
%{__rm} -rf $RPM_BUILD_ROOT%{_sysconfdir}/php/php-fpm.conf.default
%{__rm} -rf $RPM_BUILD_ROOT%{_sysconfdir}/php/php-fpm.d/www.conf.default


%files
%defattr(-,root,root)

%{_sbindir}/php-fpm
%{_bindir}/php
%{_bindir}/php-cgi
%{_bindir}/pear
%{_bindir}/peardev
%{_bindir}/pecl
%{_bindir}/phar
%{_bindir}/phar.phar

%{_libdir}/php
%{_datadir}/fpm

%{_mandir}/man1/php-cgi.1.gz
%{_mandir}/man1/php-config.1.gz
%{_mandir}/man1/php.1.gz
%{_mandir}/man1/phpize.1.gz
%{_mandir}/man8/php-fpm.8.gz
%{_mandir}/man1/phar.1.gz
%{_mandir}/man1/phar.phar.1.gz

%config(noreplace) %{_sysconfdir}/php/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php/pear.conf
%config(noreplace) %{_sysconfdir}/php/php-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/php/php.ini

%{_unitdir}/php-fpm.service

%dir %{_sysconfdir}/php
%dir %{_sysconfdir}/php/php-fpm.d

# pear files
/.channels
/.depdb
/.depdblock
/.filemap
/.lock

# 不安装源码以及phpize扩展，如果需要使用phpize安装扩展请自行调整是否安装源码文件
%exclude %{_bindir}/php-config
%exclude %{_bindir}/phpize
%exclude %{_includedir}/php
%exclude %{_libdir}/php/build

%exclude %{_libdir}/php/extensions/no-debug-non-zts-20180731/opcache.a

%files devel
%defattr(-,root,root)

%{_bindir}/php-config
%{_bindir}/phpize
%{_includedir}/php
%{_libdir}/php/build

%exclude %{_libdir}/php/extensions/no-debug-non-zts-20180731/opcache.a


%post
# init systemd 配置
/usr/bin/systemctl preset php-fpm.service >/dev/null 2>&1 ||:


%changelog
* Thu Feb 7 2019 init php rpm package <liangqi000@gmail.com> - %{version}-%{release}
- opt spec config
