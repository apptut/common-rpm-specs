Name:           php-ext-imagick
Version:        3.4.3
Release:        2%{?dist}
Summary:        php imagick.so 扩展

License: 	AGPLv3       
Source0:        %{name}-%{version}.tgz

BuildRequires:  php >= 7.0.1, autoconf, gcc-c++, make, ImageMagick-devel
Requires:       php >= 7.0.1


%description
php imagick 扩展

%prep
%setup -q -n imagick-%{version}

%build
phpize
./configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
INSTALL_ROOT=$RPM_BUILD_ROOT make install

%files
%dir %{_prefix}/include/php/ext/imagick
%{_prefix}/include/php/ext/imagick/php_imagick_shared.h
%{_prefix}/lib/php/extensions/no-debug-non-zts-20180731/imagick.so

%post
# config php.ini
exist=$(grep 'extension=imagick' /etc/php/php.ini | wc -l)
if [ $exist > 0 ]; then
    sed -i '/extension=imagick/d' /etc/php/php.ini
fi
echo 'extension=imagick' >> /etc/php/php.ini    

# restart php-fpm
php_on=$(ps -ef | grep php-fpm | grep -v 'grep' | wc -l)
if [ php_on > 0 ]; then
    systemctl restart php-fpm
fi

cat <<BANNER
----------------------------------------------------------------------

Thanks for using php-ext-imagick!

----------------------------------------------------------------------
BANNER

%preun
exist=$(grep 'extension=imagick' /etc/php/php.ini | wc -l)
if [ $exist > 0 ]; then
    sed -i '/extension=imagick/d' /etc/php/php.ini
    php_on=$(ps -ef | grep php-fpm | grep -v 'grep' | wc -l)
    if [ php_on > 0 ]; then
        systemctl restart php-fpm
    fi
fi

%postun

# delete empty dir
#rm -rf %{_includedir}/php/ext/imagick

%changelog
* Sun Feb 10 2019 扩展包初始化打包 <liangqi000@gmail.com>
- 3.4.3
