Name:           gamescope
Version:        3.12.0
Release:        1
Summary:        SteamOS session compositing window manager
Group:          System/Libraries
License:        BSD
URL:            https://github.com/Plagman/gamescope
Source0:        https://github.com/Plagman/gamescope/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/Joshua-Ashton/vkroots/archive/vkroots-26757103dde8133bab432d172b8841df6bb48155.tar.gz

BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  git
BuildRequires:  hwdata
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xres)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(wlroots)
BuildRequires:  pkgconfig(libliftoff)
BuildRequires:  pkgconfig(libcap)
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
%autosetup -p1

pushd subprojects
rm -rf vkroots
tar xf %{SOURCE1}
mv vkroots-26757103dde8133bab432d172b8841df6bb48155 vkroots
popd


%build
#sed -i '\/stb/d' meson.build
sed -i '\/force_fallback/d' meson.build # NO!
%meson   \
          -Dpipewire=enabled \
          -Denable_openvr_support=false
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_bindir}/gamescope
%{_libdir}/libVkLayer_FROG_gamescope_wsi.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_FROG_gamescope_wsi.json
