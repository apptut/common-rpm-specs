Name:           LuaJIT
Version:        2.0.5 
Release:        4%{?dist}
Summary:        luajit rpm package

License:        AGPLv3

Source0:  	LuaJIT-2.0.5.tar.gz      

BuildRequires: 	gcc 
BuildRequires: 	make

%description
luajit官方未提供rpm包，本rpm包非官方版本，本包对应官方2.0.5版本。

%prep
%setup -q

%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install PREFIX=/usr MULTILIB=lib64


%files
/usr/bin/luajit
/usr/bin/luajit-2.0.5
/usr/include/luajit-2.0/lauxlib.h
/usr/include/luajit-2.0/lua.h
/usr/include/luajit-2.0/lua.hpp
/usr/include/luajit-2.0/luaconf.h
/usr/include/luajit-2.0/luajit.h
/usr/include/luajit-2.0/lualib.h
/usr/lib64/libluajit-5.1.a
/usr/lib64/libluajit-5.1.so
/usr/lib64/libluajit-5.1.so.2
/usr/lib64/libluajit-5.1.so.2.0.5
/usr/lib64/pkgconfig/luajit.pc
/usr/share/luajit-2.0.5/jit/bc.lua
/usr/share/luajit-2.0.5/jit/bcsave.lua
/usr/share/luajit-2.0.5/jit/dis_arm.lua
/usr/share/luajit-2.0.5/jit/dis_mips.lua
/usr/share/luajit-2.0.5/jit/dis_mipsel.lua
/usr/share/luajit-2.0.5/jit/dis_ppc.lua
/usr/share/luajit-2.0.5/jit/dis_x64.lua
/usr/share/luajit-2.0.5/jit/dis_x86.lua
/usr/share/luajit-2.0.5/jit/dump.lua
/usr/share/luajit-2.0.5/jit/v.lua
/usr/share/luajit-2.0.5/jit/vmdef.lua
/usr/share/man/man1/luajit.1.gz

%changelog
