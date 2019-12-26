import os
Import("env")

STM32_FLASH_SIZE = 256

for define in env['CPPDEFINES']:
    if define[0] == "VECT_TAB_ADDR":
        env['CPPDEFINES'].remove(define)
    if define[0] == "STM32_FLASH_SIZE":
        STM32_FLASH_SIZE = define[1]

# Relocate firmware from 0x08000000 to 0x08007000
env['CPPDEFINES'].append(("VECT_TAB_ADDR", "0x08007000"))

custom_ld_script = os.path.abspath("buildroot/share/PlatformIO/ldscripts/STM32F103RC_SKR_MINI_" + str(STM32_FLASH_SIZE) + "K.ld")
for i, flag in enumerate(env["LINKFLAGS"]):
    if "-Wl,-T" in flag:
        env["LINKFLAGS"][i] = "-Wl,-T" + custom_ld_script
    elif flag == "-T":
        env["LINKFLAGS"][i + 1] = custom_ld_script

env.Append(
    ARFLAGS=["rcs"],

    ASFLAGS=["-x", "assembler-with-cpp"],

    CCFLAGS=[
        "-Wno-register",
        "-fabi-version=0",
        "-fno-use-cxa-atexit",
        "-fno-threadsafe-statics",
        "-ffast-math",
        "-Wno-unused-const-variable",
    ],
    LINKFLAGS=[
        "-Os",
        "-march=armv7-m",
        "-mcpu=cortex-m3",
        "-mfix-cortex-m3-ldrd",
        "-ffreestanding",
        "-mthumb",
        "--specs=nano.specs",
        "--specs=nosys.specs",
        "-u_printf_float",
        "--enable-newlib-io-long-long",
    ],
)