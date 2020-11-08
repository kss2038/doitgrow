from datetime import datetime
from flask import Blueprint, request, render_template, url_for, g
from werkzeug.utils import redirect
from ..forms import CommentForm
from .auth_views import login_required
from pybo.models import Comment, Question, Answer
from pybo import db

bp = Blueprint("comment", __name__, url_prefix="/comment")

@bp.route('/create/question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def question_create(question_id):
    form = CommentForm()
    if request.method == "POST" and form.validate_on_submit():
        question = Question.query.get_or_404(question_id)
        comment = Comment(content=form.content.data, user=g.user, create_date=datetime.now(), question=question)
        db.session.add(comment)
        db.session.commit()
        return redirect('{}#comment_{}'.format(url_for('question.detail', question_id=question_id), comment.id))

    return render_template('comment/comment_form.html', form=form)
        
@bp.route('/delete/question/<int:comment_id>')
def question_delete(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    question_id = comment.question.id
    if g.user != comment.user:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/modify/question/<int:comment_id>', methods=['GET', 'POST'])
def question_modify(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=comment.question.id))
    if request.method == "POST":
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()
            db.session.commit()
            return redirect('{}#comment_{}'.format(url_for('question.detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)

@bp.route('/create/answer/<int:answer_id>', methods=['GET', 'POST'])
@login_required
def answer_create(answer_id):
    form = CommentForm()
    if request.method == "POST" and form.validate_on_submit():
        answer = Answer.query.get_or_404(answer_id)
        comment = Comment(content=form.content.data, user=g.user, create_date=datetime.now(), answer=answer)
        db.session.add(comment)
        db.session.commit()
        return redirect('{}#comment_{}'.format(url_for('question.detail', question_id=comment.answer.question_id), comment.id))
    
    return render_template('comment/comment_form.html', form=form)

@bp.route('/delete/answer/<int:comment_id>')
def answer_delete(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    question_id = comment.answer.question.id
    if g.user != comment.user:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/modify/answer/<int:comment_id>', methods=['GET', 'POST'])
def answer_modify(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=comment.question.id))
    if request.method == "POST":
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()
            db.session.commit()
            return redirect('{}#comment_{}'.format(url_for('question.detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)