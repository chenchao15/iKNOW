<template>
  <div class="stage">
    <Menu style="background: #f8f8f9;width: 900px;margin-left: -39px;margin-top: -30px;z-index: 1;" mode="horizontal" theme="light" active-name="playerManagement" @on-select="chooseMenu">
      <MenuItem name="playerManagement" class="stage-menu-menuItem" style="font-size: 18px">
　　　　　　　　<Icon type="ios-people"></Icon>
        参赛者管理
      </MenuItem>
      <MenuItem name="eventHandle" class="stage-menu-menuItem" style="font-size: 18px">
        <Icon type="grid"></Icon>
        事件处理
      </MenuItem>
      <Submenu name="processManagement" class="stage-menu-menuItem" style="font-size: 18px">
        <template slot="title">
         　<Icon type="navicon-round"></Icon>
        　 过程管理
        </template>
        <MenuItem name="testUpload"　style="font-weight:500">试题上传</MenuItem>
        <MenuItem name="resultSubmit"　style="font-weight:500">参赛者提交设置</MenuItem>
     　</Submenu>
      <Submenu name="gradeManagement" class="stage-menu-menuItem" style="font-size: 18px">
        <template slot="title">
         　<Icon type="ios-paper"></Icon>
        　 成绩管理
        </template>
        <MenuItem name="gradeStatistics"　style="font-weight:500">成绩统计</MenuItem>
        <MenuItem name="gradeCheck"　style="font-weight:500">成绩批改</MenuItem>
     　</Submenu>
    </Menu>
    <div v-if="currentMenu === 'playerManagement'"><stagePlayerManagement :stageId="stageId"></stagePlayerManagement></div>
    <div v-else-if="currentMenu === 'eventHandle'"><stageEventHandle :stageId="stageId"></stageEventHandle></div>
    <div v-else-if="currentMenu === 'testUpload'"><stageTestUpload :stageId="stageId"></stageTestUpload></div>
    <div v-else-if="currentMenu === 'resultSubmit'"><stageResultSubmit :stageId="stageId"></stageResultSubmit></div>
    <div v-else-if="currentMenu === 'gradeStatistics'"><stageGradeStatistics :stageId="stageId"></stageGradeStatistics></div>
    <div v-else-if="currentMenu === 'gradeCheck'"><stageGradeCheck :stageId="stageId"></stageGradeCheck></div>
  </div>
</template>

<script>
import stagePlayerManagement from './stagePlayerManagement'
import stageEventHandle from './stageEventHandle'
import stageTestUpload from './stageTestUpload'
import stageResultSubmit from './stageResultSubmit'
import stageGradeStatistics from './stageGradeStatistics'
import stageGradeCheck from './stageGradeCheck'
export default {
  name: 'stageManage',
  props: ['stageId'],
  data () {
    return {
      stage: {},
      currentMenu: 'playerManagement'
    }
  },
  components: {
    stagePlayerManagement,
    stageEventHandle,
    stageTestUpload,
    stageResultSubmit,
    stageGradeStatistics,
    stageGradeCheck
  },
  watch: {
    stageId: function () { // 切换阶段时get
      this.currentMenu = 'playerManagement'
    }
  },
  mounted () { // 打开该页面时get
    this.currentMenu = 'playerManagement'
  },
  methods: {
    chooseMenu (menu) {
      this.currentMenu = menu
    }
  }
}
</script>

<style>
    .stage{
    }
    .stage-menuddd{
        background: #f8f8f9;
        width: 900px;
        margin-left: -39px;
        margin-top: -30px;
        z-index: 1;
    }
    .stage-menu-menuItem{
        width: 225px; 
        text-align: center; 
    }
</style>
