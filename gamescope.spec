Name:           gamescope
Version:        3.14.7
Release:        1
Summary:        SteamOS session compositing window manager
Group:          System/Libraries
License:        BSD
URL:            https://github.com/Plagman/gamescope
Source0:        https://github.com/Plagman/gamescope/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/Joshua-Ashton/vkroots/archive/vkroots-5c217cd43ca1ceecaa6acfc93a81cdc615929155.tar.gz
Source2:        https://github.com/Joshua-Ashton/reshade/archive/reshade-4245743a8c41abbe3dc73980c1810fe449359bf1.tar.gz
Source3:        https://github.com/Joshua-Ashton/wlroots/archive/wlroots-a5c9826e6d7d8b504b07d1c02425e6f62b020791.tar.gz

Patch0:         0001-cstdint.patch

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
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libeis-1.0)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(SPIRV-Headers)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(sdl2)
# Upstream decided to fork wlroots and use unstable ver. 0.18! So we need to pull subproject
BuildRequires:  pkgconfig(wlroots)
BuildRequires:  pkgconfig(libliftoff)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libdisplay-info)
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
mv vkroots-5c217cd43ca1ceecaa6acfc93a81cdc615929155 vkroots
popd
# Push in reshade from sources instead of submodule            
pushd src
rm -rf reshade
tar xf %{SOURCE2}
mv reshade-4245743a8c41abbe3dc73980c1810fe449359bf1 reshade
popd

pushd src
rm -rf wlroots
tar xf %{SOURCE3}
mv wlroots-a5c9826e6d7d8b504b07d1c02425e6f62b020791 wlroots
popd

%autopatch -p1

# Replace spirv-headers include with the system directory            
sed -i 's^../thirdparty/SPIRV-Headers/include/spirv/^/usr/include/spirv/^' src/meson.build

%build
#sed -i '\/stb/d' meson.build
#sed -i '\/force_fallback/d' meson.build # NO!
%meson   \
          -Dpipewire=enabled \
          -Denable_openvr_support=false
%meson_build

%install
%meson_install

rm -rf %{buildroot}/%{_includedir}/vkroots.h
rm -rf %{buildroot}/%{_libdir}/pkgconfig/vkroots.pc

%files
%license LICENSE
%doc README.md
%{_bindir}/gamescope
%{_libdir}/libVkLayer_FROG_gamescope_wsi_*.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_FROG_gamescope_wsi.*.json
#exclude %{datadir}/include/vkroots.h
#exclude %{libdir}/lib64/pkgconfig/vkroots.pc
