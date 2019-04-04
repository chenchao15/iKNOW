from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#组织者
class OrganizerUser(models.Model):
    user = models.OneToOneField(User, related_name = "organizer_user")
    name = models.CharField(max_length = 50, verbose_name="组织全称")
    shortname = models.CharField(max_length = 50, verbose_name="组织简称")
    introduction = models.TextField(verbose_name = "简介", )
    address = models.CharField(max_length = 50, verbose_name="地址")
    field = models.CharField(max_length = 50, verbose_name="领域")
    contact = models.CharField(max_length = 50, verbose_name="联系人姓名")
    contact_number = models.CharField(max_length = 50, verbose_name="联系人电话")
    contact_email = models.CharField(max_length = 50, verbose_name="联系人邮箱")
    avatar_url = models.CharField(default = "static/static/avatar/default_avatar.jpg", max_length = 200, verbose_name="头像地址", blank=True, null=True)

#比赛
class Competition(models.Model):
    name = models.CharField(max_length = 50, verbose_name="比赛全称")
    status = models.IntegerField(default = 0, verbose_name="比赛发布状态")
    pic_url = models.CharField(max_length = 200, verbose_name="图片地址", blank=True)
    organizer = models.ForeignKey(OrganizerUser, blank=True, related_name = "competition", verbose_name="组织者")
    detail = models.TextField(default="", verbose_name="介绍")
    objectrange = models.TextField(default="", verbose_name="参赛对象")
    objectschool = models.TextField(default="", verbose_name="参赛学校")
    category = models.IntegerField(default = 0, verbose_name="比赛类别") #unused
    sponsor = models.TextField(default="", verbose_name="主办方")
    contractor = models.TextField(default="", verbose_name="承办方")
    level = models.IntegerField(default = 0, verbose_name="比赛级别")
    #competition_system = models.TextField(default="", verbose_name="赛制")

#教程
class Tutorial(models.Model):
    status = models.IntegerField(default = 0, verbose_name="状态")
    author = models.ForeignKey(User, related_name = "tutorial", verbose_name="作者")
    title = models.CharField(default = "", max_length = 50, verbose_name="标题")
    brief = models.CharField(default = "", max_length = 50, verbose_name="简介")
    content = models.TextField(default = "", verbose_name="内容")
    post_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="发表时间")

#参赛者
class ContestantUser(models.Model):
    user = models.OneToOneField(User, related_name = "contestant_user")
    follow_competition = models.ManyToManyField(Competition, related_name = "followers", blank=True)
    join_competition = models.ManyToManyField(Competition, related_name = "joiners", blank=True)
    collect_tutorial = models.ManyToManyField(Tutorial, related_name = "collectors", blank=True)
    name = models.CharField(max_length = 50, verbose_name="真实姓名")
    nickname = models.CharField(max_length = 50, verbose_name="昵称")
    gender = models.IntegerField(default = 0, verbose_name="性别") #0 unknowen 1 male 2 female
    introduction = models.TextField(verbose_name = "简介", blank=True, null=True)
    school = models.CharField(max_length = 50, verbose_name="学校")
    major = models.CharField(max_length = 50, verbose_name="专业")
    student_number = models.CharField(max_length = 50, verbose_name="学号", blank=True, null=True)
    phone_number = models.CharField(max_length = 50, verbose_name="电话号码")
    avatar_url = models.CharField(default = "static/static/avatar/default_avatar.jpg", max_length = 200, verbose_name="头像地址", blank=True, null=True)

#教程评论
class TutorialComment(models.Model):
	author = models.ForeignKey(User, related_name = "tutorial_comment", verbose_name="作者")
	tutorial = models.ForeignKey(Tutorial, related_name = "comment", verbose_name="对应的教程")
	content = models.TextField(verbose_name="内容")
	post_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="发表时间")

#比赛评论
class CompetitionComment(models.Model):
    author = models.ForeignKey(User, related_name = "competition_comment", verbose_name="作者")
    competition = models.ForeignKey(Competition, related_name = "comment", verbose_name="对应的比赛")
    floor = models.IntegerField(default = 0, verbose_name="对应的评论id")
    link_comment = models.ForeignKey('self', related_name = "linked_comment", verbose_name="所链接的评论", blank = True, null=True)
    content = models.TextField(verbose_name="内容")
    post_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="发表时间")

#私信
class PersonalLetter(models.Model):
    sender = models.ForeignKey(User, related_name = "send_letter", verbose_name="发送者")
    receiver = models.ForeignKey(User, related_name = "receive_letter", verbose_name="接收者")
    content = models.TextField(verbose_name="内容")
    post_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="发送时间")
    is_read = models.IntegerField(verbose_name="是否已读")


class EmailToken(models.Model):
    username = models.CharField(max_length = 50, verbose_name="用户名")
    username_token = models.CharField(max_length = 100, verbose_name="用户名加密值")


class PasswordToken(models.Model):
    username = models.CharField(max_length = 50, verbose_name="用户名")
    username_token = models.CharField(max_length = 100, verbose_name="用户名加密值")


class Phase(models.Model):
    competition = models.ForeignKey(Competition, related_name = "phase")
    competition_ongoing = models.ForeignKey(Competition, related_name = "phase_ongoing", blank=True, null=True)
    competition_enrolling = models.ForeignKey(Competition, related_name = "phase_enrolling", blank=True, null=True)
    name = models.CharField(default="", max_length = 50, verbose_name="阶段名称")
    start_time = models.DateTimeField(db_index=True, verbose_name="开始时间", blank=True)
    end_time = models.DateTimeField(db_index=True, verbose_name="结束时间", blank=True)
    sign_start_time = models.DateTimeField(db_index=True, verbose_name="报名开始时间", blank=True)
    sign_end_time = models.DateTimeField(db_index=True, verbose_name="报名结束时间", blank=True)
    max_group = models.IntegerField(default = 1, verbose_name="小组最大人数")
    min_group = models.IntegerField(default = 1, verbose_name="小组最小人数")
    joiner = models.ManyToManyField(ContestantUser, related_name = "phase", blank=True)
    status = models.IntegerField(default = 0, verbose_name="状态")
    able_to_sign = models.IntegerField(default = 0, verbose_name="可报名")
    enrolment_method = models.TextField(default="", verbose_name="报名方式")
    result_submit_method = models.TextField(default="", verbose_name="结果上传")
    test_upload_method = models.TextField(default="", verbose_name="试题上传")


class Notice(models.Model):
    competition = models.ForeignKey(Competition, related_name = "notice")
    status = models.IntegerField(default = 0, verbose_name="状态") #0 stored, 1 posted, 2 deleted
    title = models.CharField(max_length = 50, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    post_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="发表时间")


class GroupMessage(models.Model):
    competition = models.ForeignKey(Competition, related_name = "group_message")
    receiver = models.ManyToManyField(ContestantUser, related_name = "group_message")
    status = models.IntegerField(default = 0, verbose_name="状态")
    title = models.CharField(max_length = 50, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    post_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="发表时间")


class Event(models.Model):
    phase = models.ForeignKey(Phase, related_name = "event")
    contestant = models.ForeignKey(ContestantUser, related_name = "event")
    is_team = models.IntegerField(default = 0, verbose_name="是否队伍")
    event_type = models.IntegerField(default = 0, verbose_name="类别") #1:报名,2:退赛,3:申诉,4:申请队长移交,5:申请队长,6申请编辑资料,7处分
    content = models.TextField(verbose_name="内容")
    time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="时间")
    status = models.IntegerField(default = 1, verbose_name="处理情况") #1:未审核,2:已通过,3:未通过
    handle_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name="处理时间")
    reason = models.TextField(default = '', verbose_name="处理内容")


class AuditEvent(models.Model):
    organizer = models.ForeignKey(OrganizerUser, related_name = "event")
    content = models.TextField(verbose_name="内容")
    time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="时间")
    status = models.IntegerField(default = 1, verbose_name="处理情况") #1:未审核,2:已通过,3:未通过
    reason = models.TextField(default = '', verbose_name="处理内容")

    
class Grade(models.Model):
    phase = models.ForeignKey(Phase, related_name = "grade")
    contestant = models.ForeignKey(ContestantUser, related_name = "grade")
    is_team = models.IntegerField(default = 0, verbose_name="是否队伍")
    content = models.TextField(default ='', verbose_name="内容")
    time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="时间")
    submit_url = models.TextField(default = "", verbose_name="提交地址")
    submit_grade = models.IntegerField(default = 0, verbose_name="成绩")
    is_handled = models.IntegerField(default = 0, verbose_name="是否批改")
    handle_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name="批改时间")
    handle_content = models.TextField(verbose_name="批改内容")


class Team(models.Model):
    phase = models.ForeignKey(Phase, related_name = "team")
    team_leader = models.ForeignKey(ContestantUser, related_name = "leader_team")
    team_member = models.ManyToManyField(ContestantUser, related_name = "member_team", blank=True)
    name = models.CharField(max_length = 50, verbose_name="队伍名称")
    introduction = models.TextField(verbose_name = "简介", blank=True, null=True)
    invitation_code = models.TextField(default = "", verbose_name = "邀请码", blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="创建时间")


class Enrolment(models.Model):
    phase = models.ForeignKey(Phase, related_name = "enrolment", blank = True)
    contestant = models.ForeignKey(ContestantUser, related_name = "enrolment", blank = True)
    enrolment_info = models.TextField(default="", verbose_name="报名信息")


class Attachment(models.Model):
    competition = models.ForeignKey(Competition, related_name = "attachment", blank=True)
    label = models.CharField(default="", max_length = 100, verbose_name="标签")
    islook = models.CharField(default="", max_length = 50, verbose_name="可见性")
    name = models.CharField(default="", max_length = 100, verbose_name="附件名称")
    attachment_url = models.CharField(default = "", max_length = 200, verbose_name="附件地址")


class CompetitionAndContestant(models.Model):
    competition = models.ForeignKey(Competition, related_name = "status_with_contestant")
    contestant = models.ForeignKey(ContestantUser, related_name = "status_with_competition")
    is_focus = models.IntegerField(default = 0, verbose_name="是否关注")
    is_joining = models.IntegerField(default = 0, verbose_name="是否参加")
    is_remind = models.IntegerField(default = 0, verbose_name="是否提醒")
    current_phase = models.ForeignKey(Phase, blank=True, null=True, related_name = "competition_contestant", verbose_name="当前阶段")
    backup = models.TextField(default = '', verbose_name="备注")
