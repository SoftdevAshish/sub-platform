from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from writer.models import Article
from .models import Subscription
from account.models import CustomUser
from .paypal import *
from .forms import UpdateUserForm


@login_required(login_url="login")
def client_dashboard(request):
    try:
        sub_details = Subscription.objects.get(user=request.user)
        subscription_plan = sub_details.subscription_plan
        context = {"SubPlan": subscription_plan}
        return render(request, "client/client-dashboard.html", context)
    except Exception as e:
        print(e)
        subscription_plan = None
        context = {"SubPlan": subscription_plan}
        return render(request, "client/client-dashboard.html", context)


@login_required(login_url="login")
def browse_articles(request):
    article = []
    try:
        subs_details = Subscription.objects.get(user=request.user, is_active=True)
    except Exception as e:
        print(e)
        return redirect("subscription-locked")
    current_subs_plan = subs_details.subscription_plan
    if current_subs_plan == "Premium":
        article = Article.objects.all()
    elif current_subs_plan == "Standard":
        article = Article.objects.all().filter(is_premium=False)
    context = {"AllClientArticle": article}
    return render(request, "client/browse-article.html", context)


@login_required(login_url="login")
def subscription_locked(request):
    return render(request, "client/subscription-lock.html")


@login_required(login_url="login")
def subscription_plans(request):
    if not Subscription.objects.filter(user=request.user).exists():
        return render(request, "client/subscription-plan.html")
    else:
        return redirect("client-dashboard")


@login_required(login_url="login")
def account_management(request):
    try:
        # Updating Our Account Details
        form = UpdateUserForm(instance=request.user)
        if request.method == "POST":
            form = UpdateUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect("client-dashboard")
        subs_details = Subscription.objects.get(user=request.user)
        subs_id = subs_details.paypal_subscription_id
        # Pass throught data  to our template
        context = {"SubID": subs_id, "UpdateUserForm": form}
        return render(request, "client/account-management.html", context)
    except Exception as e:
        print(e)
        # Updating Our Account Details
        form = UpdateUserForm(instance=request.user)
        if request.method == "POST":
            form = UpdateUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect("client-dashboard")
        context = {"UpdateUserForm": form}

        return render(request, "client/account-management.html", context)


@login_required(login_url="login")
def delete_account(request):
    if request.method == "POST":
        delete_user = CustomUser.objects.get(email=request.user)
        delete_user.delete()
        return redirect("")
    return render(request, "client/delete-account.html")


@login_required(login_url="login")
def create_subscription(request, subID, plan):
    custom_user = CustomUser.objects.get(email=request.user.email)
    if not Subscription.objects.filter(user=request.user).exists():
        first_name = custom_user.first_name
        last_name = custom_user.last_name
        full_name = first_name + " " + last_name
        print(subID, plan)
        selected_sub_plan = plan
        if selected_sub_plan == "Standard":
            sub_cost = "4.99"
        elif selected_sub_plan == "Premium":
            sub_cost = "9.99"
        subscription = Subscription.objects.create(
            subscriber_name=full_name,
            subscription_plan=selected_sub_plan,
            subscription_cost=sub_cost,
            paypal_subscription_id=subID,
            is_active=True,
            user=request.user,
        )
        context = {"SubscriptionPlan": selected_sub_plan}
        return render(request, "client/create-subscription.html", context)
    else:
        return redirect("client-dashboard")


@login_required(login_url="login")
def delete_subscription(request, subID):
    try:
        access_token = get_access_token()
        cancel_subscription_paypal(access_token, subID)
        subscription = Subscription.objects.get(
            user=request.user, paypal_subscription_id=subID
        )
        subscription.delete()

        return render(request, "client/delete-subscription.html")
    except Exception:
        return redirect("client-dashboard")


@login_required(login_url="login")
def update_subscription(request, subID):
    access_token = get_access_token()
    approved_link = update_subscription_paypal(access_token, subID)
    if approved_link:
        return redirect(approved_link)
    else:
        return HttpResponse("Unable to obtain the approved link")


@login_required(login_url="login")
def paypal_update_sub_confirmed(request):
    try:
        sub_details = Subscription.objects.get(user=request.user)
        subscriptionID = sub_details.paypal_subscription_id
        context = {"SubscriptionID": subscriptionID}
        return render(request, "client/paypal-update-sub-confirmed.html", context)
    except Exception as e:
        print(e, "Paypal-update-sub-confirm")
        return render(request, "client/paypal-update-sub-confirmed.html")


@login_required(login_url="login")
def django_update_sub_confirmed(request, subID):
    access_token = get_access_token()
    current_plan_id = get_current_subscription_paypal(access_token, subID)
    if current_plan_id == "P-0V263541YJ847252NMYZWHEI":  # Standard
        new_plan_name = "Standard"
        new_cost = "4.99"
        Subscription.objects.filter(paypal_subscription_id=subID).update(
            subscription_plan=new_plan_name, subscription_cost=new_cost
        )
    elif current_plan_id == "P-7G886984HF913452DMYZWIDQ":  # Premium
        new_plan_name = "Premium"
        new_cost = "9.99"
        Subscription.objects.filter(paypal_subscription_id=subID).update(
            subscription_plan=new_plan_name, subscription_cost=new_cost
        )
    return render(request, "client/django-update-sub-confirmed.html")


