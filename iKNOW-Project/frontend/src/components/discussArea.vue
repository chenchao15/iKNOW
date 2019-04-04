<template>
  <div>
    <div class="layout">
      <div class="layout-content">
        <p style="font-size:20px;margin-bottom:10px">评论</p>
        <Input type="textarea" v-model="commentcontent" :autosize="{minRows: 5,maxRows: 10}" placeholder="说点什么吧..."></Input>
        <Button size="large" type="text" class="send-comment" @click="sendComment">发表评论 <Icon type="chevron-right" color="#4DACF0"></Icon></Button>
      </div>
      <div class="layout-comment" v-for="(comment, index) in comments" :key="index">
        <hr color="#d7dde4" size="1" />
        <Row class="each-comment">
          <a @click="goPersonalPage(index)"><avatar class="comment-avatar" :src="comment.avatar_url" /></a>
          <a @click="goPersonalPage(index)" class="comment-name">{{comment.name}}</a>
          <span class="comment-floor">{{comment.floor}} 楼</span>
          <label class="comment-time">{{comment.post_time}}</label>
          <Button v-if="responseList[index].flag === false" type="text" size="small" class="comment-response" @click="response(index)">回复</Button>
          <Button v-else-if="responseList[index].flag === true" type="text" size="small" class="comment-response" @click="foldback(index)">收回</Button>
        </Row>
        <Row v-if="comment.link_comment !== '' && comment.link_comment !== null && comment.link_comment !== undefined">
          <span class="comment-resp">回复 {{comment.link_comment.floor}} 楼</span>
        </Row>
        <p class="comment-content" v-html="comment.content"></p>
        <div v-if="responseList[index].flag === true" style="margin-top:10px">
          <Input type="textarea" v-model="responseList[index].content" :autosize="{minRows: 5,maxRows: 10}" placeholder="对该用户评论..."></Input>
          <Button size="large" type="text" style="float:right;font-size:12px" @click="isresponse(index)">发表评论 <Icon type="chevron-right" color="#4DACF0"></Icon></Button>
        </div>
      </div>
      <div class="comment-page">
        <Page :total="this.pageNum" :current="1" page-size="5" show-elevator @on-change="changePage"></Page>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'discussArea',
  data () {
    return {
      pageNum: 0,
      currenPage: 1,
      perPage: 5,
      commentcontent: null,
      comments: [],
      responseindex: -1,
      responseList: []
    }
  },
  mounted () {
    var dataGet = {
      competition_id: this.$route.params.id
    }
    this.$http.get(this.GLOBAL.baseUrl + 'api/competition/comment_number', {params: dataGet})
    .then((response) => {
      var res = JSON.parse(response.bodyText)
      this.pageNum = res.comment_number
    })
    .catch((response) => {
      this.$Message.error('获取评论数量失败')
    })
    this.initResponseList()
    this.links()
  },
  methods: {
    links () {                      //  get讨论区评论内容列表，格式如下
      var dataGet = {
        competition_id: this.$route.params.id,
        comment_num: this.perPage,
        current_page: this.currenPage
      }
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/competition_comment', {params: dataGet})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        for (var i = 0; i < res.length; i++) {
          if (res[i].author.contestant_user === null) {
            res[i].type = 1
            res[i].name = res[i].author.organizer_user.name
            res[i].avatar_url = res[i].author.organizer_user.avatar_url
          } else {
            res[i].type = 0
            res[i].name = res[i].author.contestant_user.name
            res[i].avatar_url = res[i].author.contestant_user.avatar_url
          }
        }
        this.comments = res
        console.log(this.comments)
      })
      .catch((response) => {
        this.$Message.error('获取评论列表失败')
        this.comments = []
      })
    },
    goPersonalPage (index) {
      var type = this.comments[index].type
      var id = (type === 0 ? this.comments[index].author.contestant_user.id : this.comments[index].author.organizer_user.id)
      var mid = this.comments[index].author.id
      this.$router.push('/otherUserPage/' + mid + '/' + id + '/' + type)
    },
    sendComment () {                           // post this.commentcontent到后端
      this.initResponseList()
      if (this.commentcontent) {
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/competition_comment', {competition_id: this.$route.params.id, content: this.commentcontent})
        .then((response) => {
          this.$Notice.success({
            title: '评论成功',
            desc: `您成功发表了评论<br>评论内容：${this.commentcontent}`
          })
          this.commentcontent = null
        })
        .catch((response) => {
          this.$Notice.error({
            title: '评论失败',
            desc: `评论失败...`
          })
          this.commentcontent = null
        })
      } else {
        this.$Notice.error({
          title: '评论失败',
          desc: `您的评论内容为空，请填写内容`
        })
        this.commentcontent = null
      }
    },
    response (index) {
      this.initResponseList()
      this.responseindex = index
      this.responseList[this.responseindex].flag = true
    },
    foldback (index) {
      this.responseList[this.responseindex].flag = false
      this.initResponseList()
    },
    isresponse (index) {      // post this.responseList[this.responseindex].content到后端
      if (this.responseList[this.responseindex].content) {
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/competition_comment', {competition_id: this.$route.params.id, content: this.responseList[this.responseindex].content, comment_id: this.comments[index].id})
        .then((response) => {
          this.$Notice.success({
            title: '评论成功',
            desc: `您成功发表了评论<br>评论内容：${this.responseList[this.responseindex].content}`
          })
          this.responseList[this.responseindex].flag = false
          this.initResponseList()
        })
        .catch((response) => {
          this.$Notice.error({
            title: '评论失败',
            desc: `评论失败...`
          })
          this.responseList[this.responseindex].flag = false
          this.initResponseList()
        })
      } else {
        this.$Notice.error({
          title: '评论失败',
          desc: `您的评论内容为空，请填写内容`
        })
        this.responseList[this.responseindex].flag = false
        this.initResponseList()
      }
    },
    changePage (count) {
      this.currenPage = count
      this.initResponseList()
      this.links()
    },
    initResponseList () {
      this.responseindex = -1
      this.responseList = []
      for (var i = 0; i < 5; i++) {
        this.responseList.push({
          flag: false,
          content: null
        })
      }
    }
  }
}
</script>

<style scoped>
    .layout{
        border: 1px solid #d7dde4;
    }
    .layout-content{
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
        padding: 20px;
        padding-bottom: 0;
    }
    .layout-comment{
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
        padding: 20px;
        padding-top: 0;
    }
    .send-comment{
        float: right;
        margin: 10px 0;
        font-size: 17px;
    }
    .each-comment{
        margin-top: 20px;
    }
    .comment-avatar{
        margin-top: -6px;
        width: 40px;
        height: 40px;
        border-radius: 40px;
    }
    .comment-name{
        margin-left: 6px;
        font-size: 16px;
    }
    .comment-floor{
        margin-left: 4px;
        font-size: 14px;
        color: red;
    }
    .comment-resp{
        font-size: 14px;
        color: blue;
    }
    .comment-time{
        margin-left: 4px;
        font-size: 12px;
        color: #9ea7b4;
    }
    .comment-content{
        margin-top: 10px;
        font-size: 15px;
        color: #80848f;
    }
    .comment-response{
        float: right;
    }
    .comment-page{
        margin: 10px 0;
        overflow: hidden;
        float: right;
        font-size: 13px;
    }
</style>
