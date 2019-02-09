Name:           php
Version:        7.3.2
Release:        3%{?dist}
Summary:        php rpm 包

License:        AGPLv3 
Source0:        %{name}-%{version}.tar.gz
Source1:        php.ini

BuildRequires:  libxml2-devel
BuildRequires:  libcurl-devel >= 7.15.5
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  zlib-devel
BuildRequires:  pcre-devel


%description
基于php7官方版本制作的rpm包，该包未编译GD库，如有需要请自行安装扩展库。

%prep
%setup -q


%build
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
    	--sbindir=%{_sbindir} \
    	--sysconfdir=%{_sysconfdir}/php \
	--with-libdir=%{_lib} \
    	--with-config-file-path=%{_sysconfdir}/php \
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
	--without-pear

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

#%make_install

%files
%defattr(-,root,root)

%{_sbindir}/php-fpm
%{_bindir}/phar
%{_bindir}/phar.phar
%{_bindir}/php
%{_bindir}/php-cgi
%{_bindir}/php-config
%{_bindir}/phpdbg
%{_bindir}/phpize

%{_prefix}/lib/php/
%{_includedir}/php/
%{_datadir}/fpm

%{_mandir}/man1
%{_mandir}/man8

%config(noreplace) %{_sysconfdir}/php/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php/php-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/php/php.ini

%{_unitdir}/php-fpm.service

%dir %{_sysconfdir}/php
%dir %{_sysconfdir}/php/php-fpm.d


%post
# init systemd 配置
/usr/bin/systemctl preset php-fpm.service >/dev/null 2>&1 ||:


%changelog
* Thu Feb 7 2019 init php rpm package <liangqi000@gmail.com>
- 7.3.2
