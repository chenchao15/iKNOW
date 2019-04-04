<template>
  <div　class="basic">
    <navigationBar></navigationBar>
　　　　<h1 class="basic-title">比赛基本信息</h1> 
      <Row>
        <Col span="18" offset="3"> 
          <Form class="fontsize" ref="formValidate" :model="formValidate" :label-width="80">
　　　　　　　　　　　　<p style="font-size:16px;font-weight:bold">竞赛宣传封面</p>
            <div class="basic-image">
              <img :src="this.formValidate.imageurl"/><br><br>
              <div class="basic-image-cover">
                <Icon class="basic-icon" type="ios-eye-outline" @click.native="handleView()"></Icon>
              </div>
              <Modal title="View Image" v-model="visible" width="1200">
                <img :src="this.formValidate.imageurl" style="width:100%" v-if="visible">
              </Modal>
            </div>
            <FormItem label="比赛名称" prop="name">　
              <Input v-model="formValidate.name" placeholder="" disabled></Input>
            </FormItem>
            <FormItem label="主办方" prop="sponsor">
              <Input v-model="formValidate.sponsor" placeholder="" disabled></Input>
            </FormItem>
　　　　　　　　　　　　<div v-for="(item, index) in formValidate.otherSponsor">
              <FormItem label="" prop="otherSponsor[index]" v-if="index !== 0">
                <Input v-model="formValidate.otherSponsor[index]" placeholder="" disabled></Input>
              </FormItem>
            </div>
            <FormItem label="承办方" prop="organizer">
              <Input v-model="formValidate.organizer" placeholder="" disabled></Input>
            </FormItem>
　　　　　　　　　　　　<div v-for="(item, index) in formValidate.otherOrganizer">
              <FormItem label="" prop="otherOrganizer[index]" v-if="index !== 0">
                <Input v-model="formValidate.otherOrganizer[index]" placeholder="" disabled></Input>
              </FormItem>
            </div>
            <FormItem label="竞赛级别" prop="level">
              <RadioGroup v-model="formValidate.level">
                <Radio label="0" disabled>校级</Radio>
                <Radio label="1" disabled>市级</Radio>
　　　　　　　　　　　　　　　　<Radio label="2" disabled>省级</Radio>
　　　　　　　　　　　　　　　　<Radio label="3" disabled>国家级</Radio>
　　　　　　　　　　　　　　　　<Radio label="4" disabled>国际级</Radio>
　　　　　　　　　　　　　　　　<Radio label="5" disabled>自由</Radio>
              </RadioGroup>
            </FormItem>
            <FormItem label="参赛对象" prop="objectRange">
              <RadioGroup v-model="formValidate.objectRange">
                <Radio label="0" disabled>大学生(无限制)</Radio>
                <Radio label="1" disabled>指定高校</Radio>
              </RadioGroup>
            </FormItem>
　　　　　　　　　　　　<Row v-if="formValidate.objectRange == '1'">
              <FormItem label="高校名称" prop="objectSchool">
                <Input v-model="formValidate.objectSchool" placeholder="" disabled></Input>
              </FormItem>
            </Row>
　　　　　　　　　　　　<div v-for="(item, index) in formValidate.otherObjectSchool" v-if="formValidate.objectRange == '1'">
              <FormItem label="" prop="otherObjectSchool[index]" v-if="index !== 0">
                <Input v-model="formValidate.otherObjectSchool[index]" placeholder="" disabled></Input>
              </FormItem>
            </div>
            <FormItem label="竞赛详情" prop="detail">
              <Input v-model="formValidate.detail" type="textarea" :autosize="{minRows: 4,maxRows: 10}" placeholder="" disabled></Input>
            </FormItem>
            <FormItem>
              <Button type="primary" @click="modifyBasic">编辑</Button>
              <Button v-if="formValidate.status === 0" type="success" @click="publishIsOk" style="margin-left: 270px">发布比赛</Button>
            </FormItem>
          </Form>
        </Col>
      </Row>
    <Modal v-model="publishModal" width="500">
      <p slot="header" style="color:#2d8cf0;text-align:center">
        <Icon type="information-circled"></Icon>
        <span>确认发布比赛</span>
      </p>
      <div style="text-align:center">
        <h3 style="color: red">请确保填写比赛信息完整,包括阶段设置,比赛报名设置等</h3>
      </div>
      <div slot="footer">
        <Button type="info" size="large" long @click="publishCompetition">我已完成并确认发布比赛</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
import navigationBar from '../components/navigationBar'
export default {
  data () {
    return {
      visible: false,
      publishModal: false,
      formValidate: {
        id: -1,
        name: '',
        sponsor: '',
        otherSponsor: [''],
        otherOrganizer: [''],
        organizer: '',
        objectRange: '',
        objectSchool: '',
        otherObjectSchool: [''],
        level: '',
        detail: '',
        imageurl: '',
        status: -1
      }
    }
  },
  components: {
    navigationBar
  },
  mounted () {
    this.links()
  },
  watch: {
    '$route' (to, from) {
      if (from.path === '/createcompetition' || from.path === '/orgpage') {
        this.links()
      }
    }
  },
  methods: {
    links () {
      var res = {name: 'ss', sponsor: ['fff', 'gff'], organizer: ['gf', 'y'], objectRange: '1', objectSchool: ['qwe', 'asd'], level: '2', detail: 'dfdfsdfdfdgfgdfdfsfsdfdfsdfsdfsdf', imageurl: 'https://i.loli.net/2017/12/02/5a226834585e9.jpg', status: -1}
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/detail/' + this.$route.params.id)
          .then((response) => {
            var res0 = JSON.parse(response.bodyText)
            res.name = res0.name
            res.sponsor = JSON.parse(res0.sponsor)
            res.organizer = JSON.parse(res0.contractor)
            res.objectRange = res0.objectrange
            res.objectSchool = JSON.parse(res0.objectschool)
            res.level = res0.level
            res.detail = res0.detail
            res.imageurl = res0.pic_url
            res.status = res0.status
            this.getInfoFromRes(res)
          }).catch((response) => {
          })
      this.GLOBAL.competeBasicInfo = this.formValidate
    },
    getInfoFromRes (res) {
      var index = 0
      var len
      this.formValidate.id = this.$route.params.id
      this.formValidate.name = res.name
      this.formValidate.level = res.level
      this.formValidate.objectRange = res.objectRange
      this.formValidate.detail = res.detail
      this.formValidate.imageurl = res.imageurl
      this.formValidate.sponsor = res.sponsor[0]
      len = this.formValidate.otherSponsor.length
      this.formValidate.otherSponsor.splice(1, len - 1)
      for (index = 1; index < res.sponsor.length; index++) {
        this.formValidate.otherSponsor.push(res.sponsor[index])
      }
      this.formValidate.organizer = res.organizer[0]
      len = this.formValidate.otherOrganizer.length
      this.formValidate.otherOrganizer.splice(1, len - 1)
      for (index = 1; index < res.organizer.length; index++) {
        this.formValidate.otherOrganizer.push(res.organizer[index])
      }
      this.formValidate.objectSchool = res.objectSchool[0]
      len = this.formValidate.otherObjectSchool.length
      this.formValidate.otherObjectSchool.splice(1, len - 1)
      for (index = 1; index < res.objectSchool.length; index++) {
        this.formValidate.otherObjectSchool.push(res.objectSchool[index])
      }
      this.formValidate.status = res.status
    },
    quitSubmit () {
      this.$router.push('/home')
    },
    handleView () {
      this.visible = true
    },
    modifyBasic () {
      this.$router.push('/modifycompetitionbasic/' + this.$route.params.id)
    },
    publishIsOk () {
      var res0
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/listPhase?id=' + this.$route.params.id)
        .then((response) => {
          res0 = JSON.parse(response.bodyText)
          if (res0.length === 0) {
            this.$Notice.error({
              title: '比赛信息不完整',
              desc: '您还没有创建阶段，请在阶段管理一栏中创建一个阶段，在比赛报名设置一栏中为相应阶段设置报名表'
            })
          } else {
            this.publishModal = true
          }
        }).catch((response) => {
        })
    },
    publishCompetition () { // this.$route.params.id
      this.publishModal = false
      var data = {name: this.formValidate.name, status: 1}
      this.$http.put(this.GLOBAL.baseUrl + 'api/competition/detail/' + this.$route.params.id, data)
        .then((response) => {
          this.$Message.success('发布成功')
        }).catch((response) => {
          this.$Message.error('发布失败')
        })
    }
  }
}
</script>

<style>
    .basic{
        margin-left: 10%;
    }
    .basic-title{
        margin-left: -70px;
        margin-bottom: 20px;
    }
    .basic-label{
        font-weight: bold;
    }
    .basic-image img{
        width: 100%;
        height: 300px;
        border: 2px solid #d7dde4; 
        border-radius: 5px
    }
    .basic-image-cover{
        display: none;
        position: absolute;
        top: 24px;
        width: 100%;
        height: 300px;
        background: rgba(0,0,0,.4);
        border: 2px solid #d7dde4; 
        border-radius: 5px
    }
    .basic-image:hover .basic-image-cover{
        display: block;
    }
    .basic-icon{
        color: #f8f8f9;
        font-size: 50px;
        margin-left: 45%;
        margin-top: 100px;
        cursor: pointer;
    }
    .fontsize label{
        font-weight:bold;
        font-size: 16px !important;
    }
</style>
