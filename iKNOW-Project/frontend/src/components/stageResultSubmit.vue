<template>
  <div class="TestUpload">
    <Card class="TestUpload-Card">
      <div>
        <Form :label-width="110">
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
            <Col span="20" v-if="thing.type==='submitCount'">
              <FormItem label="每天提交次数上限" prop="name">
                <p class="TestUpload-p" v-if="thing.value === '1'">仅一次</p>
                <p class="TestUpload-p" v-if="thing.value === '2'">两次</p>
                <p class="TestUpload-p" v-if="thing.value === '3'">三次</p>
                <p class="TestUpload-p" v-if="thing.value === '4'">无限制</p>
              </FormItem>
            </Col>
            <Col span="20" v-if="thing.type==='Upload'">
              <FormItem :label="thing.name" prop="name">
                <Upload
                  type="drag"
                  action="">
                  <div style="padding: 20px 0">
                    <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
                    <p>{{thing.value}}</p>
                  </div>
                </Upload>
              </FormItem>
            </Col>
            <Col span="3">
              <Button type="text" icon="minus" @click="del(index)"></Button>
            </Col>
          </Row>
        </Form>
      </div>
      <Button type="dashed" style="font-size:20px;font-weight:bold" @click="addNewItem">更改参赛者提交方式</Button>
    </Card>
    <Button type="info" class="TestUpload-save" @click="linkPost">保存</Button>
    <Modal v-model="itemModal" width="800" @on-visible-change="modalItemRecover">
      <p slot="header" style="color:#2d8cf0;text-align:center">
        <Icon type="information-circled"></Icon>
        <span>参赛者提交方式</span>
      </p>
      <div style="text-align:center;margin-bottom: 20px">
        <h3>请选择您想使用的提交方式</h3>
        <Button class="sign-itembtn" @click="addItem.type = 'singleLine'">增加单行提示信息</Button>
        <Button class="sign-itembtn" style="margin-left: 10px" @click="addItem.type = 'multiLine'">增加多行提示信息</Button>
        <Button class="sign-itembtn" style="margin-left: 10px" @click="addItem.type = 'editTest'">在线编辑结果提交</Button>
        <Button class="sign-itembtn" style="margin-left: 10px" @click="addItem.type = 'Upload'">上传结果文件</Button>
        <Button class="sign-itembtn" style="margin-left: 10px" @click="addItem.type = 'submitCount'">提交次数限制</Button>
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
              <p class="TestUpload-p">题目：</p>
            </Col>
            <Col span="4">
            　　<p class="TestUpload-p">提交正文</p>
            </Col>
          </Row>
        </div>
        <div v-if="addItem.type === 'submitCount'">
          <Row style="margin-bottom: 10px">
            <Col span="5" offset="3">
              <p class="TestUpload-p">每天提交次数上限:</p>
            </Col>
            <Col span="4" offset="1">
            　　<Select v-model="addItem.value" style="width:200px">
                <Option value="1">1</Option>
                <Option value="2">2</Option>
                <Option value="3">3</Option>
                <Option value="4">无限制</Option>
             </Select>
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
              <p class="TestUpload-p">题目：</p>
            </Col>
            <Col span="4"> 
             　<p class="TestUpload-p">提交附件</p>
            </Col>
          </Row>
          <Row style="margin-bottom: 10px">
            <Col span="4" offset="3">
              <p class="TestUpload-p" style="margin-top: 5px">提示信息：</p>
            </Col>
            <Col span="14">
              <Input v-model="addItem.value" style="margin-top: 5px" placeholder="填入一些下载提示，也可不填"></Input>
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
        this.uploadItem = JSON.parse(res.result_submit_method)
      }).catch((response) => {
        this.uploadItemInit()
      })
    },
    uploadItemInit () {
      this.uploadItem = [
        {name: '提交附件', type: 'Upload', value: '请同学们注意提交截止时间'},
        {name: '', type: 'singleLine', value: '结果文件大小不得超过２G'},
        {name: '', type: 'submitCount', value: '3'}
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
        if (this.addItem.type === 'Upload') {
          this.addItem.name = '提交附件'
        } else if (this.addItem.type === 'editTest') {
          this.addItem.name = '提交正文'
        }
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
    linkPost () {
      var data = this.uploadItem
      this.$http.post(this.GLOBAL.baseUrl + 'api/competition/detailPhase/' + this.stageId, {result_submit_method: JSON.stringify(data)})
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
