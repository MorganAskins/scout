#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

__visible struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0xef1c5950, __VMLINUX_SYMBOL_STR(module_layout) },
	{ 0x348f4c47, __VMLINUX_SYMBOL_STR(usb_deregister) },
	{ 0x39abc14e, __VMLINUX_SYMBOL_STR(usb_register_driver) },
	{ 0xc87dfcd7, __VMLINUX_SYMBOL_STR(usb_control_msg) },
	{ 0xf8db47ed, __VMLINUX_SYMBOL_STR(mutex_unlock) },
	{ 0x487eb250, __VMLINUX_SYMBOL_STR(mutex_lock) },
	{ 0xa202a8e5, __VMLINUX_SYMBOL_STR(kmalloc_order_trace) },
	{ 0x2c2436d8, __VMLINUX_SYMBOL_STR(usb_register_dev) },
	{ 0xa2cf7a06, __VMLINUX_SYMBOL_STR(kmem_cache_alloc_trace) },
	{ 0x33cc9f44, __VMLINUX_SYMBOL_STR(kmalloc_caches) },
	{ 0x8cecd344, __VMLINUX_SYMBOL_STR(usb_deregister_dev) },
	{ 0x37a0cba, __VMLINUX_SYMBOL_STR(kfree) },
	{ 0x353ee66d, __VMLINUX_SYMBOL_STR(usb_clear_halt) },
	{ 0x4f8b5ddb, __VMLINUX_SYMBOL_STR(_copy_to_user) },
	{ 0xdb7305a1, __VMLINUX_SYMBOL_STR(__stack_chk_fail) },
	{ 0x27e1a049, __VMLINUX_SYMBOL_STR(printk) },
	{ 0x3c2cb7bd, __VMLINUX_SYMBOL_STR(usb_bulk_msg) },
	{ 0x4f6b400b, __VMLINUX_SYMBOL_STR(_copy_from_user) },
	{ 0x37d7c7ec, __VMLINUX_SYMBOL_STR(current_task) },
	{ 0xedceffc7, __VMLINUX_SYMBOL_STR(__mutex_init) },
	{ 0x9e88526, __VMLINUX_SYMBOL_STR(__init_waitqueue_head) },
	{ 0x78e739aa, __VMLINUX_SYMBOL_STR(up) },
	{ 0x6dc6dd56, __VMLINUX_SYMBOL_STR(down) },
	{ 0xbdfb6dbb, __VMLINUX_SYMBOL_STR(__fentry__) },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=usbcore";

MODULE_ALIAS("usb:v0547p1002d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v21E1p0000d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v21E1p0001d*dc*dsc*dp*ic*isc*ip*in*");
MODULE_ALIAS("usb:v21E1p0005d*dc*dsc*dp*ic*isc*ip*in*");
