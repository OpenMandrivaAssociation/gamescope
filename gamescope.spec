Name:           gamescope
Version:        3.16.17
Release:        2
Summary:        SteamOS session compositing window manager
Group:          System/Libraries
License:        BSD
URL:            https://github.com/Plagman/gamescope
Source0:        https://github.com/Plagman/gamescope/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/Joshua-Ashton/vkroots/archive/vkroots-5106d8a0df95de66cc58dc1ea37e69c99afc9540.tar.gz
Source2:        https://github.com/Joshua-Ashton/reshade/archive/reshade-696b14cd6006ae9ca174e6164450619ace043283.tar.gz
Source3:        https://github.com/Joshua-Ashton/wlroots/archive/wlroots-54e844748029d4874e14d0c086d50092c04c8899.tar.gz

#Patch0:         0001-cstdint.patch
# No need to force submodules in case of libliftoff because version packaged by OMV is exactly same as puted into submodule
Patch1:          no-submodule-for-libliftoff.patch
Patch2:          Use-system-stb-glm.patch

BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  git
BuildRequires:  hwdata
BuildRequires:  pkgconfig(benchmark)
BuildRequires:  pkgconfig(glm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xres)
BuildRequires:  pkgconfig(libavif)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libdecor-0)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libeis-1.0)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(luajit)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xwayland)
BuildRequires:  pkgconfig(SPIRV-Headers)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libinput)
# Upstream decided to fork wlroots and use unstable ver. 0.18! So we need to pull subproject
#BuildRequires:  pkgconfig(wlroots)
BuildRequires:  pkgconfig(libliftoff)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libdisplay-info)
#BuildRequires:  pkgconfig(openvr)
BuildRequires:  glslang
BuildRequires:  glslang-devel
BuildRequires:  stb-devel

Requires: %{_lib}liftoff0
Requires: x11-server-xwayland

%description
Gamescope is the micro-compositor formerly known as steamcompmgr.
In an embedded session usecase, gamescope does the same thing as steamcompmgr, but with less extra copies and latency:
It's getting game frames through Wayland by way of Xwayland, so there's no copy within X itself before it gets the frame.
It can use DRM/KMS to directly flip game frames to the screen, even when stretching or when notifications are up, removing another copy.
When it does need to composite with the GPU, it does so with async Vulkan compute, 
meaning you get to see your frame quick even if the game already has the GPU busy with the next frame.

%prep
%autosetup -p1 -a2 -N

pushd subprojects
rm -rf vkroots
tar xf %{SOURCE1}
mv vkroots-5106d8a0df95de66cc58dc1ea37e69c99afc9540 vkroots
popd
# Push in reshade from sources instead of submodule            
pushd src
rm -rf reshade
tar xf %{SOURCE2}
mv reshade-696b14cd6006ae9ca174e6164450619ace043283 reshade
popd

pushd subprojects
rm -rf wlroots
tar xf %{SOURCE3}
mv wlroots-54e844748029d4874e14d0c086d50092c04c8899 wlroots
popd

%autopatch -p1

# Replace spirv-headers include with the system directory            
sed -i 's^../thirdparty/SPIRV-Headers/include/spirv/^/usr/include/spirv/^' src/meson.build

%build
#sed -i '\/stb/d' meson.build
#sed -i '\/force_fallback/d' meson.build # NO!
#sed -i '/force_fallback_for/s/libliftoff,//' meson.build

%meson   \
          -Dpipewire=enabled \
          -Denable_openvr_support=false
%meson_build

%install
%meson_install

rm -rf %{buildroot}/%{_includedir}/vkroots.h
rm -rf %{buildroot}/%{_libdir}/pkgconfig/vkroots.pc
rm -rf %{buildroot}/usr/lib64/libwlroots.a
rm -rf %{buildroot}/usr/lib64/pkgconfig/wlroots.pc
rm -rf %{buildroot}/usr/include/wlr/
rm -rf %{buildroot}/%{_includedir}/wlroots-0.18/
rm -rf %{buildroot}/%{_libdir}/libwlroots-0.18.a
rm -rf %{buildroot}/%{_libdir}/pkgconfig/wlroots-0.18.pc


%files
%license LICENSE
%doc README.md
%{_bindir}/gamescope
%{_bindir}/gamescopestream
%{_bindir}/gamescopectl
%{_bindir}/gamescopereaper
%{_libdir}/libVkLayer_FROG_gamescope_wsi_*.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_FROG_gamescope_wsi.*.json
%{_datadir}/gamescope/scripts/
%{_datadir}/gamescope/looks/
#exclude %{datadir}/include/vkroots.h
#exclude %{libdir}/lib64/pkgconfig/vkroots.pc
