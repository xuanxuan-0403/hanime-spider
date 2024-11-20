from siui.core import SiGlobal


def show_version_message(window):
    window.LayerRightMessageSidebar().send(
        title="Welcome to xuan Hanime!",
        text="此次测试版本为 0.1.0 预览版\n"
             "欢迎学习使用!~ 记得在仓库点个star哦~",
        msg_type=1,
        icon=SiGlobal.siui.iconpack.get("ic_fluent_hand_wave_regular"),
        fold_after=5000,
        slot=lambda: window.LayerRightMessageSidebar().send("Oops, it seems that nothing will happen due to the fact "
                                                            "that this function is currently not completed.",
                                                            icon=SiGlobal.siui.iconpack.get("ic_fluent_info_regular"))
    )
