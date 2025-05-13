
import { defineStore } from 'pinia';
export const useThemeConfig = defineStore('themeConfig', {
state: (): ThemeConfigState => ({
        themeConfig:
            {"isDrawer":false,"primary":"#807B75","isIsDark":false,"topBar":"#DDDBDB","topBarColor":"#000000","isTopBarColorGradual":false,"menuBar":"#EAD6B8","menuBarColor":"#000000","menuBarActiveColor":"rgba(86, 74, 74, 0.2)","isMenuBarColorGradual":false,"columnsMenuBar":"#334054","columnsMenuBarColor":"#e6e6e6","isColumnsMenuBarColorGradual":false,"isColumnsMenuHoverPreload":false,"isCollapse":false,"isUniqueOpened":true,"isFixedHeader":true,"isFixedHeaderChange":false,"isClassicSplitMenu":false,"isLockScreen":false,"lockScreenTime":30,"isShowLogo":true,"isShowLogoChange":false,"isBreadcrumb":false,"isTagsview":true,"isBreadcrumbIcon":true,"isTagsviewIcon":true,"isCacheTagsView":true,"isSortableTagsView":true,"isShareTagsView":true,"isFooter":true,"isGrayscale":false,"isInvert":false,"isWartermark":false,"wartermarkText":"","tagsStyle":"tags-style-four","animation":"opacitys","columnsAsideStyle":"columns-round","columnsAsideLayout":"columns-vertical","layout":"classic","isRequestRoutes":true,"globalTitle":"django的校园食堂点餐","globalViceTitle":"django的校园食堂点餐","globalViceTitleMsg":"django的校园食堂点餐","globalI18n":"zh-cn","globalComponentSize":"default"}
}),
actions: {
setThemeConfig(data: ThemeConfigState) {
    this.themeConfig =
        data.themeConfig;
        },
        },
});