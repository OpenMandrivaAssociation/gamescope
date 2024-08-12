diff -uraN gamescope-3.14.29/meson.build omv-gamescope-3.14.29/meson.build
--- gamescope-3.14.29/meson.build	2024-08-09 11:17:25.000000000 +0200
+++ omv-gamescope-3.14.29/meson.build	2024-08-12 18:01:14.609237811 +0200
@@ -6,12 +6,12 @@
   default_options: [
     'cpp_std=c++20',
     'warning_level=2',
-    'force_fallback_for=wlroots,libliftoff,vkroots',
+    'force_fallback_for=wlroots,vkroots',
   ],
 )
 
 fallbacks = get_option('force_fallback_for')
-if not (fallbacks.contains('wlroots') and fallbacks.contains('libliftoff') and fallbacks.contains('vkroots'))
+if not (fallbacks.contains('wlroots') and fallbacks.contains('vkroots'))
   error('!!!"force_fallback_for" is missing entries!!!\n\tPlease do not remove entries from force_fallback_for if you are packaging the project.\n\tWe pull in these projects at specific commits/forks/builds for a reason.\n\tIf you are not packaging, remove this line to continue.')
 endif
 
