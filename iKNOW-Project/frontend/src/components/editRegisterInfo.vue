<template>
  <div>
    <div class="layout">
      <div class="layout-content">
        <Row>
            <div class="layout-content-main">
                <Row style="margin-top: 20px">
                  <Col span="10" v-for="item in signForm" :key="item.stage">
                    <p v-if="item.stage === competition.stage" class="com-stage-title">“{{item.stage}}” 报名信息</p>
                  </Col>
                  <Col style="font-size:14px;font-weight:bold;float:right">
                    <Button v-if="editflag === false" type="primary" @click="isedit">编辑 <Icon type="edit"></Icon></Button>
                    <Button v-if="editflag === true" type="primary" @click="save">保存 <Icon type="document"></Icon></Button>
                    <Button v-if="button_type !== 'start' && button_single === false" type="primary" @click="prev"><Icon type="chevron-left"></Icon> 上一步</Button>
                    <Button v-if="button_type !== 'last' && button_single === false" type="primary" @click="next">下一步 <Icon type="chevron-right"></Icon></Button>
                  </Col>
                </Row>
                <Modal v-model="returnFlag" width="300" @on-ok="confirmReturn" @on-cancel="cancelReturn">
                  <p slot="header" style="color:#2d8cf0;text-align:center;font-size:18px">
                    <Icon type="information-circled"></Icon>
                    <span>警告</span>
                  </p>
                  <p style="text-align:center">
                    <span>确认要返回上一步吗？</span>
                  </p>
                  <p style="margin-bottom:10px; text-align:center">
                    <span>返回后本页面<strong>修改的信息将不会保存</strong></span>
                  </p>
                </Modal>
                <div class="sign-content">
                  <div v-for="i in signForm" v-if="i.stage === competition.stage">
                    <Steps :current="current" style="margin-top: 20px">
                      <Step :title="info.name" v-for="info in i.steps" :key="info.name"></Step>
                    </Steps>
                    <Card class="sign-step">
                      <div v-if="editflag === false">
                        <Form ref="infoform" :label-width="100">
                          <Row v-for="(thing, index) in i.steps[current].item" :key="thing.name">
                            <Col span="20" v-if="thing.type==='Input' || thing.type==='InputLarge'">
                              <FormItem :label="thing.name" prop="name">
                                <Input disabled v-model="infoform[current].item[thing.name][0]" v-if="thing.type==='Input'" :placeholder="thing.value[0]"></Input>
                                <Input disabled v-model="infoform[current].item[thing.name][0]" v-if="thing.type==='InputLarge'" type="textarea" :autosize="{minRows: 3,maxRows: 6}" :placeholder="thing.value[0]"></Input>
                              </FormItem>
                            </Col>
                            <Col span="20" v-if="thing.type==='Radio'">
                              <FormItem :label="thing.name" prop="name">
                                <RadioGroup v-model="radioForm[index]" >
                                  <Radio disabled v-for="v in thing.value" :label="v" :key="v">{{v}}</Radio>
                                </RadioGroup>
                              </FormItem>
                            </Col>
                            <Col span="20" v-if="thing.type==='Checkbox'">
                              <FormItem :label="thing.name" prop="name">
                                <CheckboxGroup v-model="checkboxForm[index]" >
                                  <Checkbox disabled v-for="v in thing.value" :label="v" :key="v">{{v}}</Checkbox>
                                </CheckboxGroup>
                              </FormItem>
                            </Col>
                            <Col span="20" v-if="thing.type==='Select'">
                              <FormItem :label="thing.name" prop="name">
                                <Select disabled v-model="selectForm[index]" style="width:200px">
                                  <Option v-for="item in thing.value" :value="item" :key="item">{{item}}</Option>
                                </Select>
                              </FormItem>
                            </Col>
                          </Row>
                        </Form>
                      </div>
                      <div v-if="editflag === true">
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
                                <RadioGroup v-model="radioForm[index]" >
                                  <Radio v-for="v in thing.value" :label="v" :key="v">{{v}}</Radio>
                                </RadioGroup>
                              </FormItem>
                            </Col>
                            <Col span="20" v-if="thing.type==='Checkbox'">
                              <FormItem :label="thing.name" prop="name">
                                <CheckboxGroup v-model="checkboxForm[index]" >
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
      <BackTop></BackTop>
    </div>
  </div>
</template>

<script>
export default {
  name: 'editRegisterInfo',
  props: ['stageId'],
  data () {
    return {
      file: [],
      dataForm: [],
      fileUrl: '',
      radioForm: [],
      button_single: false,
      checkboxForm: [],
      selectForm: [],
      current: 0,
      returnFlag: false,
      button_type: 'start',
      editflag: false,
      stage: '',
      stageIndex: 0,
      signForm: [],
      infoform: [],
      competition: { title: '2017年APMCM亚太地区大学生数学建模竞赛赛', stage: '初赛', joinCodes: ['123', '456', '789', '101', '124'], id: 1 }
    }
  },
  created () {
    this.links()
  },
  methods: {
    // 此处要get报名管理得来的json数组,比赛id是this.competitionId；
    links () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/listPhase?id=' + this.$route.params.id)
        .then((response) => {
          this.$Message.success('成功')
          var res0 = JSON.parse(response.bodyText)
          var res = []
          for (var i = 0; i < res0.length; i++) {
            var resi = {}
            resi.id = res0[i].id
            if (parseInt(this.stageId) === parseInt(res0[i].id)) {
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
          this.getStageIndexandItem()
          this.$http.get(this.GLOBAL.baseUrl + 'api/competition/enrolment_info?id=' + this.stageId)
          .then((response) => {
            var res0 = JSON.parse(response.bodyText)
            this.dataForm = JSON.parse(res0.enrolment_info)
            this.$http.get(this.GLOBAL.baseUrl + 'api/competition/team_detail', {params: { phase_id: this.stageId }})
            .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.team_player.identity === '队员') {
                this.register_status = 'enter'
                this.removeTeamItem()
              } else {
                this.generateForm()
              }
            })
            .catch((response) => {
              this.generateForm()
              this.team_datas = []
            })
          }).catch((response) => {
          })
        }).catch((response) => {
        })
      // 将返回的已填写的注册信息表单进行dataForm = JSON.parse(),然后传递给generateForm
    },
    // links_post_form是向后台提交已经填写好的json数组infoform；该表单的格式是[{name: '个人基本信息', item: []}, {name: '比赛信息', item: []}]
    links_post_form () { // 将this.infoform改成后端按序排列的“白纸”
      var datalist = []
      for (var i in this.infoform) {
        var infoItem = this.infoform[i]
        for (var j in infoItem.item) {
          datalist.push(infoItem.item[j])
        }
      }
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/event', {phase_id: this.stageId, event_type: 6, content: JSON.stringify(datalist), is_team: 1})
      .then((response) => {
      }).catch((response) => {
        this.$Message.error('失败')
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
    isedit () {
      this.editflag = true
    },
    save () {
      this.editflag = false
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
      this.links_post_form()
      this.reinit()
      this.$router.push('/competitiondetails/' + this.$route.params.id)
    },
    prev () {
      /* if (this.editflag === true) {
        this.returnFlag = true
      } else {
        this.confirmReturn()
      } */
      this.confirmReturn()
    },
    confirmReturn () {
      this.current--
      if (this.current === 0) {
        this.button_type = 'start'
      } else {
        this.button_type = 'nolast'
      }
      this.returnFlag = false
    },
    cancelReturn () {
      this.returnFlag = false
    },
    next () {
      var flag = true
      if (this.editflag) {
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
              desc: '您编辑的信息有未填写部分，请填写完整后进行下一步'
            })
            flag = false
            break
          }
        }
      }
      if (flag) {
        this.current++
        if (this.current === this.signForm[this.stageIndex].steps.length - 1) {
          this.button_type = 'last'
        } else if (this.current === this.signForm[this.stageIndex].steps.length) {
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
        this.button_single = true
      }
    },
    generateForm () {
      this.infoform = []
      for (var i in this.signForm) {
        var stageItem = this.signForm[i]
        if (stageItem.stage === this.competition.stage) {
          for (var j in stageItem.steps) {
            var stepsItem = stageItem.steps[j]
            this.infoform.push({name: stepsItem.name, item: {}})
            for (var k in stepsItem.item) {
              var itemItem = stepsItem.item[k]
              this.infoform[j].item[itemItem.name] = this.dataForm.shift()
              if (itemItem.type === 'Radio') {
                this.radioForm[k] = this.infoform[j].item[itemItem.name][0]
              } else if (itemItem.type === 'Checkbox') {
                this.checkboxForm[k] = this.infoform[j].item[itemItem.name]
              } else if (itemItem.type === 'Select') {
                this.selectForm[k] = this.infoform[j].item[itemItem.name][0]
              }
            }
          }
        }
      }
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
        padding: 10px 30px 20px 50px;
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
        text-align: left;
        font-color: #aaa;
        font-family: "PingFang SC";
        font-size: 20px;
        font-weight: 550;
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
