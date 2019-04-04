<template>
  <div>
    <navigationBar></navigationBar>
    <div class="layout">
      <div class="layout-content">
        <Row>
            <div class="layout-content-main">
                <Row>
                    <!--<span class="com-register-title">“{{competition.title}}” </span>-->
                    <span class="com-register">比赛报名</span>
                </Row>
                <Row style="margin-top: 20px">
                  <Col span="2">
                    <p class="com-stage-title">比赛阶段：</p>
                  </Col>
                  <Col span="8" v-for="item in signForm" :key="item.stage">
                    <p v-if="item.stage === competition.stage" class="com-stage">“{{item.stage}}”</p>
                  </Col>
                  <Col style="font-size:14px;font-weight:bold;float:right">
                    <Button type="primary" @click="prev"><Icon type="chevron-left"></Icon> 上一步</Button>
                    <Button v-if="button_type === 'nolast' && register_status === 'enter'" type="primary" @click="next">下一步 <Icon type="chevron-right"></Icon></Button>
                    <Button v-if="button_type === 'last' && register_status === 'enter'" type="primary" @click="next">提交 <Icon type="chevron-right"></Icon></Button>
                    <Button v-if="register_status === 'noenter'" type="primary" @click="createTeam">创建队伍 <Icon type="chevron-right"></Icon></Button>
                  </Col>
                </Row>
                <div v-if="register_status === 'noenter'" class="sign-content">
                  <Table border height="600" :columns="team_columns" :data="team_datas"></Table>
                </div>
                <Modal v-model="enterRegister" width="300" @on-ok="isJoinTeam">
                  <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
                    <Icon type="information-circled"></Icon>
                    <span>加入队伍</span>
                  </p>
                  <p style="text-align:center">
                    <span>拥有<strong>队伍加入码</strong>才可以加入队伍哦～</span>
                  </p>
                  <p style="margin-bottom:10px; text-align:center">
                    <span>没有的话，请联系队长索要</span>
                  </p>
                  <Input v-model="retrCode" placeholder="请输入队伍加入码…"></Input>
                </Modal>
                <Modal v-model="returnFlag" width="300" @on-ok="confirmReturn" @on-cancel="cancelReturn">
                  <p slot="header" style="color:#2d8cf0; text-align:center;font-size:18px">
                    <Icon type="information-circled"></Icon>
                    <span>警告</span>
                  </p>
                  <p style="text-align:center">
                    <span>确认要返回上一步吗？</span>
                  </p>
                  <p style="margin-bottom:10px; text-align:center">
                    <span>返回后本页面填写的信息<strong>不保存</strong></span>
                  </p>
                </Modal>
                <div v-if="register_status === 'enter'" class="sign-content">
                  <div v-for="i in signForm" v-if="i.stage === competition.stage">
                    <Steps :current="current" style="margin-top: 20px">
                      <Step :title="info.name" v-for="info in i.steps" :key="info.name"></Step>
                    </Steps>
                    <Card class="sign-step">
                      <div>
                        <Form ref="infoform" :label-width="100">
                          <Row v-for="(thing, index) in i.steps[current].item" :key="thing.name">
                            <Col span="20" v-if="thing.type==='Input' || thing.type==='InputLarge'">
                              <FormItem :label="thing.name" prop="name">
                                <Input v-model="infoform[current].item[thing.name][0]" v-if="thing.type==='Input'" :placeholder="thing.value[0]"></Input>
                                <Input v-model="infoform[current].item[thing.name][0]" v-if="thing.type==='InputLarge'" type="textarea" :autosize="{minRows: 3,maxRows: 6}" :placeholder="thing.value[0]"></Input>
                              </FormItem>
                            </Col>
                            <Col span="20" v-if="thing.type==='Radio'">
                              <FormItem :label="thing.name" prop="name">
                                <RadioGroup v-model="radioForm[index]">
                                  <Radio v-for="v in thing.value" :label="v" :key="v">{{v}}</Radio>
                                </RadioGroup>
                              </FormItem>
                            </Col>
                            <Col span="20" v-if="thing.type==='Checkbox'">
                              <FormItem :label="thing.name" prop="name">
                                <CheckboxGroup v-model="checkboxForm[index]">
                                  <Checkbox v-for="v in thing.value" :label="v" :key="v">{{v}}</Checkbox>
                                </CheckboxGroup>
                              </FormItem>
                            </Col>
                            <Col span="20" v-if="thing.type==='Select'">
                              <FormItem :label="thing.name" prop="name">
                                <Select v-model="selectForm[index]" style="width:200px">
                                  <Option v-for="v in thing.value" :value="v" :key="v">{{v}}</Option>
                                </Select>
                              </FormItem>
                            </Col>
                            <Col span="20" v-if="thing.type==='Upload'">
                              <FormItem :label="thing.name" prop="name">
                                <Upload
                                :before-upload="handleUpload"
                                :data="returnIndex(thing.name)"
                                action="//jsonplaceholder.typicode.com/posts/">
                                <div style="padding: 20px 0">
                                  <Button type="ghost" icon="ios-cloud-upload-outline">{{thing.value[0]}}</Button>
                                </div>
                                </Upload>
                                <div v-if="fileUrl !== ''">文件: {{ fileUrl }} </div>
                              </FormItem>
                            </Col>
                          </Row>
                        </Form>
                      </div>
                    </Card>
                  </div>
                </div>
              </div>
        </Row>
      </div>
      <div class="layout-copy">
        2011-2017 &copy; iKNOW
      </div>
      <BackTop></BackTop>
    </div>
  </div>
</template>

<script>
import navigationBar from '../components/navigationBar'
export default {
  name: 'RegisterPage',
  data () {
    return {
      file: [],
      fileUrl: '',
      radioForm: [],
      checkboxForm: [],
      selectForm: [],
      current: 0,
      singleFlag: false,
      enterRegister: false,
      joinIndex: null,
      retrCode: null,
      returnFlag: false,
      register_status: 'noenter',
      button_type: 'nolast',
      join_status: 0,
      stage: '',
      stageIndex: 0,
      signForm: [],
      infoform: [],
      competition: { title: '2017年APMCM亚太地区大学生数学建模竞赛赛', stage: 1, joinCodes: ['123', '456', '789', '101', '124'], id: 1 },
      team_datas: [],
      team_columns: [
        {
          type: 'index',
          width: 60,
          align: 'center'
        },
        {
          title: '队伍',
          key: 'team_name',
          align: 'center',
          ellipsis: 'true',
          render: (h, params) => {
            return h('div', [
              h('Icon', {
                props: {
                  type: 'person-stalker'
                }
              }),
              h('strong', params.row.team_name)
            ])
          }
        },
        {
          title: '队长',
          key: 'leader_name',
          align: 'center',
          ellipsis: 'true',
          render: (h, params) => {
            return h('div', [
              h('Icon', {
                props: {
                  type: 'person'
                }
              }),
              h('normal', params.row.leader_name)
            ])
          }
        },
        {
          title: '队员人数',
          key: 'team_number',
          align: 'center',
          ellipsis: 'true',
          sortable: 'true'
        },
        {
          title: '创建日期',
          key: 'create_time',
          align: 'center',
          ellipsis: 'true',
          sortable: 'true'
        },
        {
          title: '操作',
          key: 'action',
          width: 250,
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'primary',
                  size: 'small'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.show(params.index)
                  }
                }
              }, '查看详情'),
              h('Button', {
                props: {
                  type: 'success',
                  size: 'small'
                },
                style: {
                  marginRight: '5px'
                },
                on: {
                  click: () => {
                    this.join(params.index)
                  }
                }
              }, '加入队伍'),
              h('Button', {
                props: {
                  type: 'info',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.contact(params.index)
                  }
                }
              }, '联系队长')
            ])
          }
        }
      ]
    }
  },
  components: {
    navigationBar
  },
  created () {
    this.links()
  },
  methods: {
    // 此处要get报名管理得来的json数组；
    // 报名页面是从比赛详情页眺转过来的，需要从报名详情页传递到此处一个比赛id，然后通过比赛id获取该比赛状态，比如上面的competition那两个状态是必须的
    links () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/listPhase?id=' + this.$route.params.comid)
          .then((response) => {
            this.$Message.success('成功')
            var res0 = JSON.parse(response.bodyText)
            var res = []
            for (var i = 0; i < res0.length; i++) {
              var resi = {}
              resi.id = res0[i].id
              if (parseInt(this.$route.params.stageid) === parseInt(res0[i].id)) {
                this.competition.stage = res0[i].name
              }
              resi.stage = res0[i].name
              resi.issingle = '小组赛'
              this.singleFlag = false
              if (res0[i].max_group === 1 && res0[i].min_group === 1) {
                resi.issingle = '个人赛'
                this.singleFlag = true
                this.register_status = 'enter'
              }
              if (res0[i].enrolment_method) {
                resi['steps'] = JSON.parse(res0[i].enrolment_method)
              } else {
                resi['steps'] = [{name: '个人基本信息', item: []}, {name: '比赛相关信息', item: []}]
              }
              res.push(resi)
            }
            this.signForm = res
            this.stage = this.competition.stage
            if (this.singleFlag === false) {
              this.getTeams()
            }
            this.getStageIndexandItem()
            this.generateForm()
          }).catch((response) => {
          })
      if (this.singleFlag) {
        this.register_status = 'enter'
      }
    },
    getCookie (name) {
      let reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)')
      let arr
      if ((arr = document.cookie.match(reg))) {
        return decodeURIComponent(arr[2])
      }
    },
    // links_post_form是向后台提交已经填写好的json数组infoform；该表单的格式是[{name: '个人基本信息', item: {}}}, {name: '比赛信息', item: {}}}]
    links_post_form () {
      // 将this.infoform改成后端按序排列的“白纸”
      var dataForm = []
      for (var i in this.infoform) {
        var infoItem = this.infoform[i]
        for (var j in infoItem.item) {
          dataForm.push(infoItem.item[j])
        }
      }
      var teamId = -1
      if (this.team_datas !== null && this.team_datas !== [] && this.team_datas[this.joinIndex] !== undefined) {
        teamId = this.team_datas[this.joinIndex].team_id
      }
      var data = {phase_id: this.$route.params.stageid, enrolment_info: JSON.stringify(dataForm), join_status: this.join_status, team_id: teamId}
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/enroll', data)
      .then((response) => {
      }).catch((response) => {
      })
    },
    // 获取队伍列表get
    getTeams () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/team', {params: { phase_id: this.$route.params.stageid }})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.team_datas = res.team_datas
        for (var i in this.team_datas) {
          this.team_datas[i].leader_name = this.team_datas[i].team_leader.name
        }
      })
      .catch((response) => {
        this.$Message.error('获取队伍列表失败')
        this.team_datas = []
      })
    },
    handleUpload (file) {
      this.file = file
      this.fileUrl = file.name
      return false
    },
    returnIndex (index) {
      this.infoform[this.current].item[index][0] = this.fileUrl
    },
    prev () {
      if (this.register_status === 'noenter') {
        this.reinit()
        this.$router.push('/competitiondetails/' + this.$route.params.comid)
      } else {
        // this.returnFlag = true
        this.confirmReturn()
      }
    },
    confirmReturn () {
      if (this.current === 0) {
        if (this.register_status === 'noenter' || this.singleFlag) {
          this.reinit()
          this.$router.push('/competitiondetails/' + this.$route.params.comid)
        } else {
          // this.emptyPartOfForm(this.current)
          this.register_status = 'noenter'
        }
      } else {
        // this.emptyPartOfForm(this.current)
        this.current--
        this.button_type = 'nolast'
      }
      this.returnFlag = false
    },
    cancelReturn () {
      this.returnFlag = false
    },
    next () {
      var flag = true
      for (var j in this.signForm) {
        var stageItem = this.signForm[j]
        if (stageItem.stage === this.competition.stage) {
          for (var k in stageItem.steps[this.current].item) {
            var itemItem = stageItem.steps[this.current].item[k]
            if (itemItem.type === 'Radio') {
              this.infoform[this.current].item[itemItem.name][0] = this.radioForm[k]
            } else if (itemItem.type === 'Checkbox') {
              this.infoform[this.current].item[itemItem.name] = this.checkboxForm[k]
            } else if (itemItem.type === 'Select') {
              this.infoform[this.current].item[itemItem.name][0] = this.selectForm[k]
            }
          }
        }
      }
      var list = this.infoform[this.current].item
      for (var i in list) {
        if (list === null || list[i].length === 0 || list[i][0] === null || list[i][0] === undefined || list[i][0] === '') {
          this.$Notice.error({
            title: '操作失败',
            desc: '您有内容未填写，请填写完整后进行下一步'
          })
          flag = false
          break
        }
      }
      if (flag) {
        if (this.current === this.signForm[this.stageIndex].steps.length - 2) {
          this.button_type = 'last'
        } else if (this.current === this.signForm[this.stageIndex].steps.length - 1) {
          this.links_post_form()
          this.reinit()
          this.$router.push('/competitiondetails/' + this.$route.params.comid)
        }
        this.current++
        if (this.current === this.signForm[this.stageIndex].steps.length) {
          this.current = 0
        }
      }
    },
    getStageIndexandItem () {
      var index
      var len = this.signForm.length
      for (index = 0; index < len; index++) {
        if (this.stage === this.signForm[index].stage) {
          this.stageIndex = index
        }
      }
      if (this.signForm[this.stageIndex].steps.length === 1) {
        this.button_type = 'last'
      }
    },
    generateForm () {
      this.infoform = []
      for (var i in this.signForm) {
        var stageItem = this.signForm[i]
        if (stageItem.stage === this.competition.stage) {
          for (var j in stageItem.steps) {
            var stepsItem = stageItem.steps[j]
            console.log(stepsItem.name)
            this.infoform.push({name: stepsItem.name, item: {}})
            for (var k in stepsItem.item) {
              var itemItem = stepsItem.item[k]
              this.infoform[j].item[itemItem.name] = []
              if (itemItem.type === 'Radio') {
                this.radioForm[k] = itemItem.value[0]
              } else if (itemItem.type === 'Checkbox') {
                this.checkboxForm[k] = [] // itemItem.value[0]
              } else if (itemItem.type === 'Select') {
                this.selectForm[k] = itemItem.value[0]
              }
            }
          }
        }
      }
    },
    emptyPartOfForm (index) {
      // [{name: '个人基本信息', item: {}}, {name: '比赛信息', item: {}}]
      var stepsItem = this.infoform[index]
      stepsItem.name = null
      stepsItem.item = {}
    },
    createTeam () {
      this.register_status = 'enter'
    },
    show (index) {
      this.$Modal.info({
        title: '队伍信息',
        content: `队伍名称：${this.team_datas[index].team_name}<br>队长姓名：${this.team_datas[index].leader_name}<br>队员人数：${this.team_datas[index].team_number}<br>创建时间：${this.team_datas[index].create_time}`
      })
    },
    join (index) {
      this.joinIndex = index
      this.enterRegister = true
    },
    isJoinTeam () {
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/invitation_code', {team_id: this.team_datas[this.joinIndex].team_id, invitation_code: this.retrCode})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        if (res.is_join === 1) {
          this.register_status = 'enter'
          this.removeTeamItem()
          this.join_status = 1
          this.$Notice.success({
            title: '加入码正确',
            desc: '加入码正确，请继续完成资料填写以便于加入队伍'
          })
        } else {
          this.$Notice.error({
            title: '加入失败',
            desc: '不好意思，该加入码已失效，请重新输入'
          })
        }
      })
      .catch((response) => {
        this.$Message.error('加入失败')
        this.team_datas = []
      })
      this.retrCode = null
      this.enterRegister = false
    },
    contact (index) {
      var type = 0
      var id = this.team_datas[index].team_leader.id
      var mid = this.team_datas[index].team_leader.uid
      this.$router.push('/otherUserPage/' + mid + '/' + id + '/' + type)
    },
    removeTeamItem () {
      var first = 0
      var second = 0
      for (var i in this.signForm) {
        var stageItem = this.signForm[i]
        if (stageItem.stage === this.competition.stage) {
          first = i
          for (var j in stageItem.steps) {
            var stepsItem = stageItem.steps[j]
            if (stepsItem.name === '基本信息') {
              second = j
              break
            }
          }
        }
      }
      this.signForm[first].steps.splice(parseInt(second), 1)
      this.getStageIndexandItem()
      this.generateForm()
    },
    reinit () {
    }
  }
}
</script>
<style>
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        margin-top: 2%;
    }
    .layout-logo{
        width: 100px;
        height: 30px;
        background: #5b6270;
        border-radius: 3px;
        float: left;
        position: relative;
        top: 15px;
        left: 20px;
    }
    .layout-nav{
        width: 420px;
        margin: 0 auto;
    }
    .layout-assistant{
        width: 300px;
        margin: 0 auto;
        height: inherit;
    }
    .layout-breadcrumb{
        padding: 10px 15px 0;
    }
    .layout-content{
        min-height: 100%;
        margin: 15px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
    }
    .layout-content-main{
        padding: 50px 30px 20px 50px;
    }
    .ivu-col-span-15{
        width: 100%;
    }
    .layout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
    .sign-content{
        margin-top: 20px;
        padding: 20px;
        border: 1px solid #d7dde4;
        border-radius: 6px;
    }
    .com-stage-title{
        font-color: #aaa;
        font-family: "PingFang SC";
        font-size: 16px;
        font-weight: 500;
        margin-top: 4px;
    }
    .com-stage{
        font-size: 18px;
        text-align: left;
        color: #666;
        font-weight: 600;
        overflow: hidden;
        margin: 4px 0 0 -5px;
    }
    .sign-step{
        font-weight: bold;
        margin: 20px 35px 20px 0px;
        padding: 20px;
    }
    .com-register-title{
        text-align: center;
        font-size: 25px;
        color: #666;
        font-weight: 600;
        overflow: hidden;
    }
    .com-register{
        font-size: 25px;
        font-color: #aaa;
        font-family: "PingFang SC";
    }
</style>
