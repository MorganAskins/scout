#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

struct module __this_module
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
	{ 0x14522340, "module_layout" },
	{ 0x4f1939c7, "per_cpu__current_task" },
	{ 0xd2037915, "dev_set_drvdata" },
	{ 0xd691cba2, "malloc_sizes" },
	{ 0xab2a6ec4, "usb_deregister_dev" },
	{ 0x3758301, "mutex_unlock" },
	{ 0xffc7c184, "__init_waitqueue_head" },
	{ 0xced66309, "usb_deregister" },
	{ 0x4bf79039, "__mutex_init" },
	{ 0xea147363, "printk" },
	{ 0x85f8a266, "copy_to_user" },
	{ 0xb4390f9a, "mcount" },
	{ 0xdd508520, "usb_register_dev" },
	{ 0x3461b433, "usb_control_msg" },
	{ 0xfee8a795, "mutex_lock" },
	{ 0x748caf40, "down" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0x2611da1, "usb_bulk_msg" },
	{ 0x69b3b9c9, "usb_clear_halt" },
	{ 0x2044fa9e, "kmem_cache_alloc_trace" },
	{ 0x37a0cba, "kfree" },
	{ 0x3f1899f1, "up" },
	{ 0x251ce55e, "usb_register_driver" },
	{ 0x3302b500, "copy_from_user" },
	{ 0xa92a43c, "dev_get_drvdata" },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=";

MODULE_ALIAS("usb:v0547p1002d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v21E1p0000d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v21E1p0001d*dc*dsc*dp*ic*isc*ip*");
MODULE_ALIAS("usb:v21E1p0005d*dc*dsc*dp*ic*isc*ip*");

MODULE_INFO(srcversion, "8D9E1150BB67F8447FD6216");

static const struct rheldata _rheldata __used
__attribute__((section(".rheldata"))) = {
	.rhel_major = 6,
	.rhel_minor = 8,
	.rhel_release = 641,
};
