<template>
  <div class="TestUpload">
    <Card class="TestUpload-Card">
      <div>
        <Form :label-width="100"> 
          <Row v-for="(thing,index) in uploadItem" :key="thing.name">
            <Col span="20" v-if="thing.type==='singleLine' || thing.type==='multiLine'">
              <FormItem label="提示信息" prop="name">
                <p class="TestUpload-p" style="width: 400px;word-break:break-all; word-wrap:break-word;" v-html="thing.value">{{thing.value}}</p>
              </FormItem>
            </Col>
            <Col span="20" v-if="thing.type==='editTest'">
              <FormItem :label="thing.name" prop="name">
                <Input type="textarea" v-model="thing.value" :autosize="{minRows: 20,maxRows: 100}"></Input>
              </FormItem>
            </Col>
            <Col span="20" v-if="thing.type==='Upload'">
              <FormItem :label="thing.name" prop="name">
                <Upload
                  :before-upload="handleUpload"
                  action="//jsonplaceholder.typicode.com/posts/">
                  <Button type="ghost" icon="ios-cloud-upload-outline">组织者请在此处上传相应试题</Button>
                 </Upload>
                <div v-if="fileUrl !== ''">文件: {{ fileUrl }} </div>
              </FormItem>
            </Col>
            <Col span="3">
              <Button type="text" icon="minus" @click="del(index)"></Button>
            </Col>
          </Row>
        </Form>
      </div>
      <Button type="dashed" style="font-size:20px;font-weight:bold" @click="addNewItem">更改上传方式</Button>
    </Card>
    <Button type="info" class="TestUpload-save" @click="linkPost">保存</Button>
    <Modal v-model="itemModal" width="800" @on-visible-change="modalItemRecover">
      <p slot="header" style="color:#2d8cf0;text-align:center">
        <Icon type="information-circled"></Icon>
        <span>上传方式</span>
      </p>
      <div style="text-align:center;margin-bottom: 20px">
        <h3>请选择您想使用的上传方式</h3>
        <Button class="sign-itembtn" @click="addItem.type = 'singleLine'">增加单行提示信息</Button>
        <Button class="sign-itembtn" style="margin-left: 10px" @click="addItem.type = 'multiLine'">增加多行提示信息</Button>
        <Button class="sign-itembtn" style="margin-left: 10px" @click="addItem.type = 'editTest'">在线编辑试题</Button>
        <Button class="sign-itembtn" style="margin-left: 10px" @click="addItem.type = 'Upload'">上传试题</Button>
      </div>
      <div style="text-align:center">
        <Row v-if="addItem.type === 'singleLine'">
          <Col span="3" offset="3">
            <p class="TestUpload-p">提示信息：</p>
          </Col>
          <Col span="15">
            <Input v-model="addItem.value" placeholder="填入一些提示信息，如＂请同学们注意时间截止日期＂"></Input>
          </Col>
        </Row>
        <div v-if="addItem.type === 'editTest'">
          <Row style="margin-bottom: 10px">
            <Col span="4" offset="3">
              <p class="TestUpload-p">试题题目：</p>
            </Col>
            <Col span="15">
            <Input v-model="addItem.name" placeholder="填入试题的题目"></Input>
            </Col>
          </Row>
        </div>
        <div v-if="addItem.type === 'multiLine'">
          <Row style="margin-bottom: 10px">
            <Col span="3" offset="3">
              <p class="TestUpload-p">提示信息：</p>
            </Col>
          </Row>
          <Input style="width: 600px" v-model="addItem.value" type="textarea" :autosize="{minRows: 3,maxRows: 5}" placeholder="填入一些提示信息，如＂请同学们严格按照规范做题，否则一律按０分处理＂"></Input>
        </div>
        <div v-if="addItem.type === 'Upload'">
          <Row style="margin-bottom: 10px">
            <Col span="4" offset="3">
              <p class="TestUpload-p">试题名称：</p>
            </Col>
            <Col span="14"> 
              <Input v-model="addItem.name" placeholder="填入试题名称"></Input>
            </Col>
          </Row>
        </div>
      </div>
      <div slot="footer">
        <Button type="info" size="large" long @click="addItemBtn">添加</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
export default {
  name: 'player',
  props: ['stageId'],
  data () {
    return {
      uploadItem: [],
      itemModal: false,
      test: '',
      file: [],
      fileUrl: '',
      addItem: {
        name: '',
        type: '',
        value: ''
      }
    }
  },
  mounted () {
    this.links()
  },
  methods: {
    links () {
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/detailPhase/' + this.stageId)
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.uploadItem = JSON.parse(res.test_upload_method)
        for (var i = 0; i < this.uploadItem.length; i++) {
          if (this.uploadItem[i].type === 'Upload') {
            this.fileUrl = this.uploadItem[i].fileUrl
          }
        }
      }).catch((response) => {
        this.uploadItemInit()
      })
    },
    uploadItemInit () {
      this.uploadItem = [
        {name: '', type: 'singleLine', value: '请同学们在此处下载本阶段的试题'},
        {name: '大数据竞赛', type: 'Upload', value: '点击上传本阶段试题', fileUrl: ''}
      ]
    },
    del (index) {
      this.uploadItem.splice(index, 1)
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
      } else if (this.concludeRepeat(this.addItem.type)) {
        this.$Notice.error({
          title: '重复使用组件错误',
          desc: '您只能使用一次该组件'
        })
        this.addItem.name = ''
        this.addItem.type = ''
        this.addItem.value = ''
      } else {
        this.itemModal = false
        var arr = {
          'name': this.addItem.name,
          'type': this.addItem.type,
          'value': ''
        }
        var index
        for (index = 0; index < this.addItem.value.length; index++) {
          if (this.addItem.value[index] === '\n') {
            arr.value += '<br/>'
          } else {
            arr.value += this.addItem.value[index]
          }
        }
        this.uploadItem.push(arr)
      }
    },
    concludeRepeat (type) {
      var index
      for (index = 0; index < this.uploadItem.length; index++) {
        if (this.uploadItem[index].type === type && (type === 'editTest' || type === 'Upload')) {
          return true
        }
      }
      return false
    },
    modalItemRecover (value) {
      if (value === false) {
        this.addItem.name = ''
        this.addItem.type = ''
        this.addItem.value = ''
      }
    },
    handleUpload (file) {
      this.file = file
      this.fileUrl = file.name
      return false
    },
    linkPost () {
      var data = this.uploadItem
      var index
      var formData = new FormData()
      if (this.file.length === 0) {
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/detailPhase/' + this.stageId, {test_upload_method: JSON.stringify(data)})
        .then((response) => {
          this.$Message.success('保存上传成功')
        }).catch((response) => {
          this.$Message.success('保存上传失败')
        })
      } else {
        for (index = 0; index < data.length; index++) {
          if (data[index].type === 'Upload') {
            formData.append('file', this.file, this.file.name)
            this.$http.post(this.GLOBAL.baseUrl + 'api/competition/attachment_upload', formData)
            .then((response) => {
              var res = JSON.parse(response.bodyText)
              data[index].fileUrl = res.attachment_url
              this.$http.post(this.GLOBAL.baseUrl + 'api/competition/detailPhase/' + this.stageId, {test_upload_method: JSON.stringify(data)})
              .then((response) => {
                this.$Message.success('保存上传成功')
              }).catch((response) => {
                this.$Message.success('保存上传失败')
              })
            }).catch((response) => {
            })
            break
          }
        }
      }
    }
  }
}
</script>

<style>
    .TestUpload{
    }
    .TestUpload-Card{
        font-weight: bold;
        margin-left: 60px;
        margin-top:50px;
        z-index: 0
    }
    .TestUpload-save{
        margin: 20px 20px 0 670px;
    }
    .TestUpload-p{
        margin-top: 3px;
        font-size: 17px;
    }
</style>

