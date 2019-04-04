<template>
  <div class="file">
    <h1>附件上传管理</h1>
    <div class="file-content">
      <h2 class="file-upload-title">上传新文件</h2>
      <Row style="margin-bottom:20px">
        <Col span="2" offset="1">
          <p>选择标签</p>
        </Col>
        <Col span="12">
          <Select v-model="fileForm.label" placeholder="标签可以帮助您更好地管理您的附件"　filterable>
            <Option v-for="item in labelList" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>
        </Col>
        <Col span="5" offset="1">
          <Button type="info" @click="addLabel">添加新标签</Button>
        </Col>
      </Row>
      <Form :model="fileForm" :label-width="91">
        <FormItem label="附件名称">
          <Input v-model="fileForm.name" placeholder="Enter something..."></Input>
        </FormItem>
        <FormItem label="对谁可见">
          <RadioGroup v-model="fileForm.islook">
            <Radio label="所有人(包括游客)">所有人(包括游客)</Radio>
            <Radio label="所有登录用户">所有登录用户</Radio>
            <Radio label="参加本比赛的所有参赛者">参加本比赛的所有参赛者</Radio>
            <Radio label="入围本阶段的所有参赛者">入围本阶段的所有参赛者</Radio>
          </RadioGroup>
        </FormItem>
      </Form>
      <Upload
        multiple
        :on-success="handleSuccess"
        :on-error="handleFail"
        :action="this.GLOBAL.baseUrl + 'api/competition/attachment_upload'"
        :headers="{
          'X-CSRFToken':cookie
        }">
        <Button style="margin-left: 30px" type="info" size="large" icon="ios-cloud-upload-outline">点击上传文件</Button>
      </Upload>
      <Button style="margin-left: 540px" type="success" size="large" @click="handleSavePost">保存提交</Button>
      <h2 class="file-list-title">文件列表</h2>
      <Table height="300" :columns="fileColumns" :data="fileData"></Table>
    </div>
    <Modal v-model="labelModal" width="360">
      <p slot="header" style="color:#2d8cf0;text-align:center">
        <Icon type="information-circled"></Icon>
        <span>添加新标签</span>
      </p>
      <div style="text-align:center">
        <h3>请输入新标签名称</h3>
        <Input v-model="newLabel" placeholder="如＇初赛＇,＇复赛＇等"></Input>
      </div>
      <div slot="footer">
        <Button type="info" size="large" @click="addLabelChick">确定</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import expandRow from '../components/expand-row.vue'
export default {
  name: 'fileManage',
  components: { expandRow },
  data () {
    return {
      labelList: [],
      labelModal: false,
      newLabel: '',
      cookie: '',
      fileForm: {
        name: '',
        islook: '',
        label: '',
        attachmentUrl: ''
      },
      fileColumns: [
        {
          type: 'expand',
          width: 50,
          render: (h, params) => {
            return h(expandRow, {
              props: {
                row: params.row
              }
            })
          }
        },
        {
          type: 'index',
          width: 50,
          align: 'center'
        },
        {
          title: '附件名称',
          key: 'name',
          align: 'center'
        },
        {
          title: '对谁可见',
          key: 'islook',
          align: 'center'
        },
        {
          title: '对应标签',
          key: 'label',
          align: 'center'
        }
      ],
      fileData: [
      ]
    }
  },
  mounted () {
    this.cookie = this.getCookie('csrftoken')
    this.links()
  },
  methods: {
    links () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/list_attachment?id=' + this.$route.params.id)
          .then((response) => {
            var res0 = JSON.parse(response.bodyText)
            var index
            this.labelList = []
            for (index = 0; index < res0.length; index++) {
              if (this.isHave(res0[index].label)) {
                continue
              } else {
                this.labelList.push({value: res0[index].label, label: res0[index].label})
              }
            }
            this.fileData = res0
          }).catch((response) => {
            this.$Message.error('失败')
          })
    },
    getCookie (name) {
      let reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)')
      let arr
      if ((arr = document.cookie.match(reg))) {
        return decodeURIComponent(arr[2])
      }
    },
    isHave (label) {
      var len = this.labelList.length
      var index
      for (index = 0; index < len; index++) {
        if (label === this.labelList[index].label) {
          return true
        }
      }
      return false
    },
    handleSuccess (res, file) {
      this.fileForm.attachmentUrl = res.attachment_url
    },
    handleSavePost () {
      if (this.fileForm.name === '' || this.fileForm.islook === '' || this.fileForm.attachmentUrl === '') {
        this.$Message.warning('您还有未填写的信息')
      } else {
        this.linkPost(this.fileForm)
      }
    },
    handleFail (file) {
      this.$Message.error('上传失败，请重新上传')
    },
    addLabel () {
      this.labelModal = true
    },
    addLabelChick () {
      if (!this.isHave(this.newLabel)) {
        this.labelList.push({value: this.newLabel, label: this.newLabel})
      } else {
        this.$Notice.error({
          title: '无法添加标签',
          desc: '标签名已存在'
        })
      }
      this.newLabel = ''
      this.labelModal = false
    },
    linkPost (file) {
      var data = {
        cmp_id: this.$route.params.id,
        name: file.name,
        islook: file.islook,
        label: file.label,
        attachment_url: file.attachmentUrl
      }
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/create_attachment', data)
          .then((response) => {
            this.links()
            this.$Message.success('提交成功')
          }).catch((response) => {
          })
    }
  }
}
</script>
<style>
    .file{
        font-weight: bold;
    }
    .file-content{
        margin-top: 30px;
        border: 2px solid #d7dde4;
        border-radius: 5px;
        padding: 20px;
    }
    .file-upload-title{
        margin-left: 10px;
        margin-bottom: 20px;
    }
    .file-list-title{
        margin-left: 10px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
</style>
