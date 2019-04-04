<template>
  <div>
    <h1>比赛报名设置</h1>
    <Row style="margin-top: 20px">
      <Col span="2">
        <p class="sign-select">比赛阶段</p>
      </Col>
      <Col span="10">
        <Select v-model="stage" filterable @on-change="getStageIndexandItem">
          <Option v-for="item in signForm" :value="item.stage" :key="item.stage">{{ item.stage }}</Option>
        </Select>
      </Col>
      <Col span="12">
        <Button v-if="this.signForm.length === 0" type="primary" style="font-size:14px;font-weight:bold;margin-left: 40px" @click="next">下一步</Button>
        <Button v-else-if="this.signForm.length !== 0 && this.current !== this.signForm[this.stageIndex].steps.length - 1" type="primary" style="font-size:14px;font-weight:bold;margin-left: 40px" @click="next">下一步</Button>
        <Button v-else type="primary" style="font-size:14px;font-weight:bold;margin-left: 40px" @click="next">返　回</Button>
        <Button type="dashed" style="font-size:14px;font-weight:bold;margin-left: 10px" @click="addNewStep">添加新步骤</Button>
      </Col>
    </Row>
    <div class="sign-content">
      <p v-if="this.isNoData()" class="sign-isNoData" style="text-align:center; font-size:17px; font-weight:bold;color:#9ea7b4">请选择比赛阶段</p>
      <div v-for="(i, index) in signForm" v-if="stage === i.stage">
        <Steps :current="current" style="margin-top: 20px">
          <Step :title="info.name" v-for="info in i.steps" :key="info.name"></Step>
        </Steps>
        <Card class="sign-step">
          <div>
            <Form ref="formValidate" :model="formValidate" :label-width="100">
              <Row v-for="(thing,index) in i.steps[current].item" :key="thing.name">
                <Col span="20" v-if="thing.type==='Input' || thing.type==='InputLarge'">
                  <FormItem :label="thing.name" prop="name">
                    <Input v-if="thing.type==='Input'" :placeholder="thing.value[0]"></Input>
                    <Input v-if="thing.type==='InputLarge'" type="textarea" :autosize="{minRows: 3,maxRows: 6}" :placeholder="thing.value[0]"></Input>
                  </FormItem>
                </Col>
                <Col span="20" v-if="thing.type==='Radio' || thing.type==='Checkbox'">
                  <FormItem :label="thing.name" prop="name">
                    <Radio v-for="v in thing.value" v-if="thing.type==='Radio'" :key="thing.name">{{v}}</Radio>
                    <Checkbox v-for="v in thing.value" v-if="thing.type==='Checkbox'" :key="thing.name">{{v}}</Checkbox>
                  </FormItem>
                </Col>
                <Col span="20" v-if="thing.type==='Select'">
                  <FormItem :label="thing.name" prop="name">
                    <Select v-model="model1" style="width:200px">
                      <Option v-for="item in thing.value" :value="item" :key="item">{{ item }}</Option>
                    </Select>
                  </FormItem>
                </Col>
                <Col span="20" v-if="thing.type==='Upload'">
                  <FormItem :label="thing.name" prop="name">
                    <Upload
                    type="drag"
                    action="">
                    <div style="padding: 20px 0">
                    <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
                    <p>{{thing.value[0]}}</p>
                    </div>
                  </Upload>
                  </FormItem>
                </Col>
                <Col span="3" v-if="!(i.issingle === '小组赛' && index < 2 && current === 0)">
                  <Button type="text" icon="minus" @click="del(index)"></Button>
                </Col>
              </Row>
            </Form>
          </div>
          <Button type="dashed" style="font-size:20px;font-weight:bold" @click="addNewItem">添加新组件</Button>
        </Card>
        <Button type="info" class="sign-btn" style="margin-left:600px;margin-top:30px" @click="linkSavePost">保存</Button>
        <Modal v-model="modifyModal" width="360">
          <p slot="header" style="color:#2d8cf0;text-align:center">
            <Icon type="information-circled"></Icon>
            <span>修改步骤名称</span>
          </p>
          <div style="text-align:center">
            <h3>请输入修改后的步骤名称</h3>
            <Input v-model="modifyStepName" :placeholder="i.steps[current].name"></Input>
          </div>
          <div slot="footer">
            <Button type="info" size="large" @click="modify">确定</Button>
          </div>
        </Modal>
        <Modal v-model="addModal" width="360">
          <p slot="header" style="color:#2d8cf0;text-align:center">
            <Icon type="information-circled"></Icon>
            <span>添加新步骤</span>
          </p>
          <div style="text-align:center">
            <h3>请输入新步骤的名称</h3>
            <Input v-model="addStepName" placeholder=" "></Input>
          </div>
          <div slot="footer">
            <Button type="info" size="large" long @click="add">确定</Button>
          </div>
        </Modal>
        <Modal v-model="itemModal" width="800" @on-visible-change="modalItemRecover">
          <p slot="header" style="color:#2d8cf0;text-align:center">
            <Icon type="information-circled"></Icon>
            <span>增加新组件</span>
          </p>
          <div style="text-align:center;margin-bottom: 20px">
            <h3>请选择您需要的组件</h3>
            <Button class="sign-itembtn" @click="addItem.type = 'Input'">文本输入框</Button>
            <Button class="sign-itembtn" style="margin-left: 10px" @click="addItem.type = 'Radio'">单选框</Button>
            <Button class="sign-itembtn" style="margin-left: 10px" @click="addItem.type = 'Checkbox'">多选框</Button>
            <Button class="sign-itembtn" style="margin-left: 10px" @click="addItem.type = 'Select'">下拉选择框</Button>
            <Button class="sign-itembtn" style="margin-left: 10px" @click="addItem.type = 'InputLarge'">多行文本框</Button>
            <Button class="sign-itembtn" style="margin-left: 10px" @click="addItem.type = 'Upload'">上传附件</Button>
          </div>
          <div style="text-align:center">
            <Row v-if="addItem.type === 'Input'">
              <Col span="3" offset="3">
                <p class="sign-p">组件名称：</p>
              </Col>
              <Col span="4"> 
                <Input v-model="addItem.name" placeholder="填入组件的标签"></Input>
              </Col>
              <Col span="10" offset="1">
                <Input v-model="addItem.value[0]" placeholder="填入一些提示信息"></Input>
              </Col>
            </Row>
            <div v-if="addItem.type === 'Checkbox' || addItem.type === 'Radio'">
              <Row style="margin-bottom: 10px">
                <Col span="3" offset="8">
                  <p class="sign-p">组件名称：</p>
                </Col>
                <Col span="4">
                  <Input v-model="addItem.name" placeholder="填入组件的标签"></Input>
                </Col>
              </Row>
              <Row v-for="(r, index) in modalCount" :key="index" style="margin-bottom: 10px">
                <Col span="3" offset="4">
                  <p class="sign-p">选项名称：</p>
                </Col>
                <Col span="4">
                  <Input v-model="addItem.value[index]" placeholder=""></Input>
                </Col>
                <Col span="8">
                  <Checkbox style="margin-top: 7px" v-if="addItem.type === 'Checkbox'">{{addItem.value[index]}}</Checkbox>
                  <Radio style="margin-top: 7px" v-else>{{addItem.value[index]}}</Radio>
                </Col>
                <Col span="2">
                  <Button type="text" icon="plus-round" @click="modalCountAdd" v-if="index === 0">(增加)</Button>
                  <Button type="text" icon="minus" @click="modalCountSub(index)" v-else-if="index === 1">(删除)</Button>
                </Col>
              </Row>
            </div>
            <div v-if="addItem.type === 'InputLarge'">
              <Row style="margin-bottom: 10px">
                <Col span="3" offset="8">
                  <p class="sign-p">组件名称：</p>
                </Col>
                <Col span="4">
                  <Input v-model="addItem.name" placeholder="填入组件的标签"></Input>
                </Col>
              </Row>
              <Input style="width: 600px" v-model="addItem.value[0]" type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="填入一些提示信息"></Input>
            </div>
            <div v-if="addItem.type === 'Select'">
              <Row style="margin-bottom: 10px">
                <Col span="3" offset="8">
                  <p class="sign-p">组件名称：</p>
                </Col>
                <Col span="4">
                  <Input v-model="addItem.name" placeholder="填入组件的标签"></Input>
                </Col>
              </Row>
              <Row v-for="(r, index) in modalCount" :key="index" style="margin-bottom: 10px">
                <Col span="3" offset="8">
                  <p class="sign-p">选项名称：</p>
                </Col>
                <Col span="4">
                  <Input v-model="addItem.value[index]" placeholder=""></Input>
                </Col>
                <Col span="2">
                  <Button type="text" icon="plus-round" @click="modalCountAdd" v-if="index === 0">(增加)</Button>
                  <Button type="text" icon="minus" @click="modalCountSub(index)" v-else-if="index === 1">(删除)</Button>
                </Col>
              </Row>
            </div>
            <div v-if="addItem.type === 'Upload'">
              <Row style="margin-bottom: 10px">
                <Col span="3" offset="3">
                <p class="sign-p">组件名称：</p>
              </Col>
              <Col span="4"> 
                <Input v-model="addItem.name" placeholder="填入组件的标签"></Input>
              </Col>
              <Col span="10" offset="1">
                <Input v-model="addItem.value[0]" placeholder="填入一些提示信息"></Input>
              </Col>
              </Row>
            </div>
          </div>
          <div slot="footer">
            <Button type="info" size="large" long @click="addItemBtn">添加</Button>
          </div>
        </Modal>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'signManage',
  data () {
    return {
      current: 0,
      signNum: 0,
      modifyModal: false,
      addModal: false,
      itemModal: false,
      modifyStepName: '',
      addStepName: '',
      stage: '',
      stageIndex: 0,
      signForm: [],
      formValidate: {
        name: '',
        school: '',
        major: '',
        grade: '',
        email: '',
        identify: ''
      },
      addItem: {
        name: '',
        type: '',
        value: ['']
      },
      modalCount: ['']
    }
  },
  mounted () {
    this.links()
    this.isNoData()
  },
  methods: {
    links () {
      var res = []
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/listPhase?id=' + this.$route.params.id)
          .then((response) => {
            var res0 = JSON.parse(response.bodyText)
            var res1 = []
            for (var i = 0; i < res0.length; i++) {
              var resi = {}
              resi.id = res0[i].id
              resi.stage = res0[i].name
              resi.issingle = '小组赛'
              if (res0[i].max_group === 1 && res0[i].min_group === 1) {
                resi.issingle = '个人赛'
              }
              if (res0[i].enrolment_method) {
                resi['steps'] = JSON.parse(res0[i].enrolment_method)
              } else {
                if (resi.issingle === '个人赛') {
                  resi['steps'] = [{name: '基本信息', item: []}, {name: '比赛相关信息', item: []}]
                } else {
                  resi['steps'] = [{name: '队伍基本信息', item: []}, {name: '个人基本信息', item: []}]
                }
              }
              res1.push(resi)
            }
            res = res1
            this.signForm = res
            this.signNum = res.length
          }).catch((response) => {
          })
    },
    next () {
      if (this.current === this.signForm[this.stageIndex].steps.length - 1) {
        this.current = 0
      } else {
        this.current += 1
      }
    },
    modifyStep () {
      this.modifyModal = true
    },
    modify () {
      this.signForm[this.stageIndex].steps[this.current].name = this.modifyStepName
      this.modifyStepName = ''
      this.modifyModal = false
    },
    addNewStep () {
      if (this.signForm[this.stageIndex].steps.length < 4) {
        this.addModal = true
      } else {
        this.$Notice.error({
          title: '步骤过多',
          desc: '最多四个步骤'
        })
      }
    },
    add () {
      var arr = {name: this.addStepName, item: []}
      this.signForm[this.stageIndex].steps.push(arr)
      this.addModal = false
      this.addStepName = ''
    },
    getStageIndexandItem () {
      var index
      var len = this.signForm.length
      for (index = 0; index < len; index++) {
        if (this.stage === this.signForm[index].stage) {
          this.stageIndex = index
        }
      }
      len = this.signForm[this.stageIndex].steps.length
      for (index = 0; index < len; index++) {
        if (this.signForm[this.stageIndex].steps[index].item.length === 0) {
          var item
          if (index === 0) {
            if (this.signForm[this.stageIndex].issingle === '个人赛') {
              item = [
                {name: '姓名', type: 'Input', value: ['请输入姓名']},
                {name: '学校', type: 'Input', value: ['请输入所在学校']},
                {name: '专业', type: 'Input', value: ['请输入所学专业']},
                {name: '年级', type: 'Input', value: ['请输入所在年级']},
                {name: '手机号码', type: 'Input', value: ['请输入手机号码']},
                {name: '邮箱', type: 'Input', value: ['请输入常用邮箱']},
                {name: '身份证号', type: 'Input', value: ['我们仅用于防止多账号做弊行为,绝不会透露用户个人信息']},
                {name: '身份证正面照', type: 'Upload', value: ['我们仅用于防止多账号做弊行为,绝不会透露用户个人信息']}
              ]
            } else if (this.signForm[this.stageIndex].issingle === '小组赛') {
              item = [
                {name: '队伍名称', type: 'Input', value: ['请输入队伍名称']},
                {name: '队伍简介', type: 'InputLarge', value: ['可以填写队伍成员的相关信息，所得荣誉等']},
                {name: '指导老师姓名', type: 'Input', value: ['请输入队伍指导老师姓名']},
                {name: '指导老师邮箱', type: 'Input', value: ['请输入队伍指导老师邮箱']},
                {name: '指导老师电话', type: 'Input', value: ['请输入队伍指导老师电话']},
                {name: '队伍参赛历史', type: 'Radio', value: ['从未参加', '参加过一次,有些经验', '多次参加，经验丰富']},
                {name: '队伍曾获荣誉', type: 'InputLarge', value: ['可以填写曾经获得的奖项，荣誉称号等']},
                {name: '荣誉证明', type: 'Upload', value: ['可上传成绩单或获奖证书的照片']}
              ]
            }
          } else if (index === 1) {
            if (this.signForm[this.stageIndex].issingle === '个人赛') {
              item = [
                {name: '参赛历史', type: 'Radio', value: ['从未参加', '参加过一次,有些经验', '多次参加，经验丰富']},
                {name: '曾获荣誉', type: 'InputLarge', value: ['可以填写曾经获得的奖项，荣誉称号等']},
                {name: '荣誉证明', type: 'Upload', value: ['可上传成绩单或获奖证书的照片']}
              ]
            } else if (this.signForm[this.stageIndex].issingle === '小组赛') {
              item = [
                {name: '姓名', type: 'Input', value: ['请输入姓名']},
                {name: '学校', type: 'Input', value: ['请输入所在学校']},
                {name: '专业', type: 'Input', value: ['请输入所学专业']},
                {name: '年级', type: 'Input', value: ['请输入所在年级']},
                {name: '手机号码', type: 'Input', value: ['请输入手机号码']},
                {name: '邮箱', type: 'Input', value: ['请输入常用邮箱']},
                {name: '身份证号', type: 'Input', value: ['我们仅用于防止多账号做弊行为,绝不会透露用户个人信息']},
                {name: '身份证正面照', type: 'Upload', value: ['我们仅用于防止多账号做弊行为,绝不会透露用户个人信息']}
              ]
            }
          }
          this.signForm[this.stageIndex].steps[index].item = item
        }
      }
    },
    del (index) {
      this.signForm[this.stageIndex].steps[this.current].item.splice(index, 1)
    },
    isNoData () {
      if (this.stage === '') {
        return true
      } else {
        return false
      }
    },
    addNewItem () {
      this.itemModal = true
    },
    addItemBtn () {
      if (this.addItem.type === '') {
        this.$Notice.error({
          title: '错误',
          desc: '您还没有选择组件'
        })
      } else if (this.addItem.name === '') {
        this.$Notice.error({
          title: '输入错误',
          desc: '组件名称不能为空'
        })
      } else if ((this.addItem.type === 'Radio' || this.addItem.type === 'Checkbox' || this.addItem.type === 'Select') && this.addItem.value[0] === '') {
        this.$Notice.error({
          title: '输入错误',
          desc: '组件选项不能为空,至少填一项'
        })
      } else {
        this.itemModal = false
        var arr = {
          name: this.addItem.name,
          type: this.addItem.type,
          value: this.addItem.value
        }
        this.signForm[this.stageIndex].steps[this.current].item.push(arr)
      }
    },
    modalCountAdd () {
      this.modalCount.push('')
    },
    modalCountSub (index) {
      var len = this.modalCount.length - 1
      this.modalCount.splice(len, 1)
      this.addItem.value.pop()
    },
    modalItemRecover (value) {
      if (value === false) {
        this.addItem.name = ''
        this.addItem.type = ''
        this.addItem.value = ['']
        this.modalCount = ['']
      }
    },
    linkSavePost () {
      var arr = this.signForm[this.stageIndex]
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/detailPhase/' + arr.id, {name: arr.stage, enrolment_method: JSON.stringify(arr.steps)})
          .then((response) => {
            this.$Message.success('保存成功')
          }).catch((response) => {
            this.$Message.error('保存失败')
          })
    }
  }
}
</script>
<style>
  .sign-content{
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #d7dde4;
    border-radius: 6px;
  }
  .sign-select{
    font-size: 14px;
    font-weight: bold;
    margin-top: 4px;
  }
  .sign-step{
    font-weight: bold;
    margin: 20px 35px 20px 0px;
    padding: 20px;
  }
  .sign-isisNoData{
    text-align: center; 
    font-size:17px;
    font-weight: bold;
    color: #9ea7b4;
  }
  .sign-additembtn{
    font-size: 18px;
  }
  .sign-p{
    font-size: 14px;
    font-weight: bold;
    margin-top: 5px;
  }
</style>
