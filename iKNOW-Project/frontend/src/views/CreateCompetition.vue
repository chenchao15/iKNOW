<template>
  <div>
    <navigationBar></navigationBar>
    <div class="layout">
      <div class="layout-content">
　　　　　　　　<h1 class="latout-title">创建我的比赛</h1>
        <Row>
          <Col span="16"> 
            <div class="layout-content-main">
              <Form class="fontsize" ref="formValidate" style="font-weight: bold" :model="formValidate" :rules="ruleValidate" :label-width="100">
　　　　　　　　　　　　　　　　<p style="font-size:16px">竞赛宣传封面(选填)</p>
　　　　　　　　　　　　　　　　<Upload style="margin-left:20px"
                  type="drag"
                  :show-upload-list="false"
　　　　　　　　　　　　　　　　　　:on-success="handleSuccess"
                  :on-error="handleFail"
                  :format="['jpg','jpeg','png','bmp']"
                  :max-size="4096"
                  :on-format-error="handleFormatError"
                  :on-exceeded-size="handleMaxSize"
                  :action="this.GLOBAL.baseUrl + 'api/competition/cover_upload'"
                  :headers="{
                     'X-CSRFToken':cookie
                  }">
                  <div style="padding: 20px 0" v-if="this.choose === 0">
                    <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
                    <p>Click or drag files here to upload</p>
                  </div>
                  <div v-if="this.choose === 1">
                    <img style="width:100%;height:100%;" :src="formValidate.imageurl"/>
                  </div>
                </Upload><br>
                <FormItem label="比赛名称" prop="name">　
                  <Input v-model="formValidate.name" placeholder="请输入比赛名称"></Input>
                </FormItem>
                <Row>
                  <Col span="22">
                    <FormItem label="主办方" prop="sponsor">
                  　　  <Input v-model="formValidate.sponsor" placeholder="请输入主办方"></Input>
                　　  </FormItem>
                  </Col>
                  <Col span="2">
                    <Button type="text" icon="plus-round" @click="add(formValidate.othersponsor)"></Button>
                  </Col>
                </Row>
　　　　　　　　　　　　　　　　<div v-for="(item, index) in formValidate.othersponsor">
                  <Row>
                    <Col span="22">
                      <FormItem label="" prop="othersponsor[index]" v-if="index !== 0">
                  　　    <Input v-model="formValidate.othersponsor[index]" placeholder="请输入其他主办方"></Input>
                　　    </FormItem>
                    </Col>
                    <Col span="2">
                      <Button type="text" icon="minus" v-if="index === 1" @click="sub(formValidate.othersponsor)"></Button>
                    </Col>
                  </Row>
                </div>
                <Row>
                  <Col span="22">
                    <FormItem label="承办方" prop="organizer">
                  　　  <Input v-model="formValidate.organizer" placeholder="请输入承办方"></Input>
                　　  </FormItem>
                  </Col>
                  <Col span="2">
                    <Button type="text" icon="plus-round" @click="add(formValidate.otherorganizer)"></Button>
                  </Col>
                </Row>
　　　　　　　　　　　　　　　　<div v-for="(item, index) in formValidate.otherorganizer">
                  <Row>
                    <Col span="22">
                      <FormItem label="" prop="otherorganizer[index]" v-if="index !== 0">
                  　　    <Input v-model="formValidate.otherorganizer[index]" placeholder="请输入其他承办方"></Input>
                　　    </FormItem>
                    </Col>
                    <Col span="2">
                      <Button type="text" icon="minus" v-if="index === 1" @click="sub(formValidate.otherorganizer)"></Button>
                    </Col>
                  </Row>
                </div>
                <FormItem label="竞赛级别" prop="level">
                  <RadioGroup v-model="formValidate.level">
                    <Radio label="0">校级</Radio>
                    <Radio label="1">市级</Radio>
　　　　　　　　　　　　　　　　　　　　<Radio label="2">省级</Radio>
　　　　　　　　　　　　　　　　　　　　<Radio label="3">国家级</Radio>
　　　　　　　　　　　　　　　　　　　　<Radio label="4">国际级</Radio>
　　　　　　　　　　　　　　　　　　　　<Radio label="5">自由</Radio>
                  </RadioGroup>
                </FormItem>
                <FormItem label="参赛对象" prop="objectrange">
                  <RadioGroup v-model="formValidate.objectrange">
                    <Radio label="0">大学生(无限制)</Radio>
                    <Radio label="1">指定高校</Radio>
                  </RadioGroup>
                </FormItem>
　　　　　　　　　　　　　　　　<Row v-if="formValidate.objectrange == '1'">
                  <Col span="20" offset="2">
                    <FormItem label="高校名称" prop="objectschool">
                  　　  <Input v-model="formValidate.objectschool" placeholder="请输入高校名称"></Input>
                　　  </FormItem>
                  </Col>
                  <Col span="2">
                    <Button type="text" icon="plus-round" @click="add(formValidate.otherobjectschool)"></Button>
                  </Col>
                </Row>
　　　　　　　　　　　　　　　　<div v-for="(item, index) in formValidate.otherobjectschool" v-if="formValidate.objectrange == '1'">
                  <Row>
                    <Col span="22">
                      <FormItem label="" prop="otherobjectschool[index]" v-if="index !== 0">
                  　　    <Input v-model="formValidate.otherobjectschool[index]" placeholder="请输入其他高校名称"></Input>
                　　    </FormItem>
                    </Col>
                    <Col span="2">
                      <Button type="text" icon="minus" v-if="index === 1" @click="sub(formValidate.otherobjectschool)"></Button>
                    </Col>
                  </Row>
                </div>
                <FormItem label="竞赛详情" prop="detail">
                  <Input v-model="formValidate.detail" type="textarea" :autosize="{minRows: 4,maxRows: 10}" placeholder="关于竞赛的介绍..."></Input>
                </FormItem>
                <FormItem>
                  <Button type="primary" @click="handleSubmit('formValidate')">创建</Button>
　　　　　　　　　　　　　　　　　　<Button type="ghost" @click="quitSubmit()" style="margin-left: 8px">取消</Button>
                  <Button type="ghost" @click="handleReset('formValidate')" style="margin-left:188px">重置</Button>
                </FormItem>
              </Form>
            </div>
          </Col>
        </Row>
      </div>
      <div class="layout-copy">
        2011-2017 &copy; iKNOW
      </div>
    </div>
  </div>
</template>
<script>
import navigationBar from '../components/navigationBar'
export default {
  data () {
    return {
      choose: 0,
      cookie: this.getCookie('csrftoken'),
      formValidate: {
        id: -1,
        name: '',
        sponsor: '',
        othersponsor: [''],
        otherorganizer: [''],
        organizer: '',
        objectrange: '',
        objectschool: '',
        otherobjectschool: [''],
        level: '',
        detail: '',
        imageurl: ''
      },
      ruleValidate: {
        name: [
          { required: true, message: '竞赛名称不能为空', trigger: 'blur' }
        ],
        sponsor: [
          { required: true, message: '主办方不能为空', trigger: 'blur' }
        ],
        organizer: [
          { required: true, message: '承办方不能为空', trigger: 'blur' }
        ],
        level: [
          { required: true, message: '请选择竞赛级别', trigger: 'change' }
        ],
        objectrange: [
          { required: true, message: '请选择参赛对象', trigger: 'change' }
        ],
        objectschool: [
          { required: true, message: '高校名称不能为空', trigger: 'blur' }
        ],
        detail: [
          { required: true, message: '请填写竞赛详情', trigger: 'blur' },
          { type: 'string', min: 20, message: '不得少于20个字', trigger: 'blur' }
        ]
      }
    }
  },
  components: {
    navigationBar
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/createcompetition') {
        this.cookie = this.getCookie('csrftoken')
        this.$refs['formValidate'].resetFields()
        this.formValidate.othersponsor = ['']
        this.formValidate.otherorganizer = ['']
        this.formValidate.otherobjectschool = ['']
        this.choose = 0
      }
    }
  },
  methods: {
    getCookie (name) {
      let reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)')
      let arr
      if ((arr = document.cookie.match(reg))) {
        return decodeURIComponent(arr[2])
      }
    },
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          var sponsor = []
          var organizer = []
          var objectschool = []
          this.mergeValue(sponsor, organizer, objectschool)
          var data = {name: this.formValidate.name, sponsor: JSON.stringify(sponsor), contractor: JSON.stringify(organizer), level: this.formValidate.level, objectrange: this.formValidate.objectrange, objectschool: JSON.stringify(objectschool), detail: this.formValidate.detail, pic_url: this.formValidate.imageurl}
          this.$http.post(this.GLOBAL.baseUrl + 'api/competition/create', data)
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            this.formValidate.id = res.id
            this.GLOBAL.competeBasicInfo = this.formValidate
            this.$router.push('/competitionmanage/' + res.id)
          }).catch((response) => {

          })
          this.$Message.success('创建成功')
        } else {
          this.$Message.error('创建失败')
        }
      })
    },
    quitSubmit () {
      this.$router.push('/home')
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    },
    mergeValue (sponsor, organizer, objectschool) {
      var index
      sponsor.push(this.formValidate.sponsor)
      for (index = 1; index < this.formValidate.othersponsor.length; index++) {
        sponsor.push(this.formValidate.othersponsor[index])
      }
      organizer.push(this.formValidate.organizer)
      for (index = 1; index < this.formValidate.otherorganizer.length; index++) {
        organizer.push(this.formValidate.otherorganizer[index])
      }
      objectschool.push(this.formValidate.objectschool)
      for (index = 1; index < this.formValidate.otherobjectschool.length; index++) {
        objectschool.push(this.formValidate.otherobjectschool[index])
      }
    },
    add (type) {
      type.push('')
    },
    sub (type) {
      type.pop()
    },
    handleSuccess (res, file) {
      this.formValidate.imageurl = res.pic_url
      this.choose = 1
      this.$Message.success('上传成功')
    },
    handleFail (file) {
      this.$Message.success('上传失败，请重新上传')
    },
    handleFormatError (file) {
      this.$Notice.warning({
        title: '文件类型错误',
        desc: '文件' + file.name + '的格式或类型不正确, 请上传图片格式文件(jpg,jpeg,png or bmp).'
      })
    },
    handleMaxSize (file) {
      this.$Notice.warning({
        title: '文件大小错误',
        desc: '文件' + file.name + '过大, 请上传不超过4M的文件.'
      })
    }
  }
}
</script>

<style scoped>
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        margin-top: 2%;
    }
    .latout-title{
        margin-left: 30px;
    }
    .layout-content{
        min-height: 100%;
        margin: 15px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
        padding-left: 170px;
        padding-top: 20px;
    }
    .layout-content-main{
        padding: 30px 30px 20px 100px;
    }
    .layout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
    .ivu-icon ivu-icon-plus-round{
        cursor: pointer;
    }
    .fontsize label{
        font-size: 16px !important;
    }
</style>
