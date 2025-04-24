from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.timezone import now
from django.db.models import Q
from .models import Client, Sector, Status, Organization

def home_view(request):
    return render(request, "polls/home.html")

@login_required
def relationship_system_view(request):
    tab = request.GET.get("tab", "clients")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_client":
            client_id = request.POST.get("client_id")
            client = get_object_or_404(Client, id=client_id)
            client.name = request.POST.get("name")
            client.position = request.POST.get("position")
            client.email = request.POST.get("email")
            client.phone_number = request.POST.get("phone")
            org_id = request.POST.get("organization")
            if org_id:
                client.organization = get_object_or_404(Organization, id=org_id)
            client.save()

            new_sector = request.POST.get("sector")
            sector_instance = client.sector_set.first()
            if sector_instance:
                sector_instance.sector = new_sector
                sector_instance.save()
            else:
                Sector.objects.create(client=client, sector=new_sector)

            new_status = request.POST.get("status")
            status_instance = client.status_set.first()
            if status_instance:
                status_instance.status = new_status
                status_instance.time = now()
                status_instance.save()
            else:
                Status.objects.create(client=client, status=new_status)

            return redirect("relationship_system")

        elif action == "delete_client":
            client_id = request.POST.get("client_id")
            client = get_object_or_404(Client, id=client_id)
            client.delete()
            return redirect("relationship_system")

        elif action == "add_client":
            organization = Organization.objects.first()
            Client.objects.create(
                name="",
                position="",
                email="",
                phone_number="",
                organization=organization if organization else None,
            )
            return redirect("relationship_system")

        elif action == "update_organization":
            org_id = request.POST.get("org_id")
            org = get_object_or_404(Organization, id=org_id)
            org.organization_name = request.POST.get("organization_name")
            org.type_of_organization = request.POST.get("type_of_organization")
            org.country_of_operation = request.POST.get("country_of_operation")
            org.organization_size = request.POST.get("organization_size") or 0
            org.revenue_size = request.POST.get("revenue_size") or 0
            org.website_url = request.POST.get("website_url")
            org.social_media = request.POST.get("social_media")
            org.save()
            return redirect("/relationshipsystem/?tab=organizations")

        elif action == "delete_organization":
            org_id = request.POST.get("org_id")
            org = get_object_or_404(Organization, id=org_id)
            org.delete()
            return redirect("/relationshipsystem/?tab=organizations")

        elif action == "add_organization":
            Organization.objects.create(
                organization_name="",
                type_of_organization="",
                country_of_operation="",
                organization_size=0,
                revenue_size=0,
                website_url="",
                social_media="",
            )
            return redirect("/relationshipsystem/?tab=organizations")

    # Client Filters
    clients = Client.objects.select_related("organization").prefetch_related("sector_set", "status_set")
    query = request.GET.get("q", "")
    selected_sector = request.GET.get("sector", "")
    selected_status = request.GET.get("status", "")
    selected_org = request.GET.get("organization", "")

    if query:
        clients = clients.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(position__icontains=query) |
            Q(organization__organization_name__icontains=query)
        )

    if selected_org:
        clients = clients.filter(organization__id=selected_org)

    if selected_sector:
        clients = [c for c in clients if c.sector_set.first() and c.sector_set.first().sector == selected_sector]

    if selected_status:
        clients = [c for c in clients if c.status_set.first() and c.status_set.first().status == selected_status]

    # Org Filters
    raw_orgs = Organization.objects.all()
    organizations = raw_orgs

    org_query = request.GET.get("org_q", "")
    org_type_filter = request.GET.get("org_type", "")
    country_filter = request.GET.get("org_country", "")

    if org_query:
        organizations = organizations.filter(
            Q(organization_name__icontains=org_query) |
            Q(type_of_organization__icontains=org_query) |
            Q(country_of_operation__icontains=org_query) |
            Q(website_url__icontains=org_query) |
            Q(social_media__icontains=org_query)
        )

    if org_type_filter:
        organizations = organizations.filter(type_of_organization__iexact=org_type_filter)

    if country_filter:
        organizations = organizations.filter(country_of_operation__iexact=country_filter)

    # Options for dropdowns
    org_type_options = raw_orgs.values_list("type_of_organization", flat=True).distinct()
    country_options = raw_orgs.values_list("country_of_operation", flat=True).distinct()

    return render(
        request,
        "polls/relationship_system.html",
        {
            "tab": tab,
            "clients": clients,
            "organizations": organizations,
            "raw_orgs": raw_orgs,
            "sector_choices": Sector.SectorChoices.choices,
            "status_choices": Status._meta.get_field("status").choices,
            "query": query,
            "selected_sector": selected_sector,
            "selected_status": selected_status,
            "selected_org": selected_org,
            "org_query": org_query,
            "org_type_filter": org_type_filter,
            "country_filter": country_filter,
            "org_type_options": org_type_options,
            "country_options": country_options,
        },
    )

# Form view
@csrf_exempt
def public_client_form(request):
    if request.method == "POST":
        # Get or create organization
        org_name = request.POST.get("organization_name")
        organization, _ = Organization.objects.get_or_create(
            organization_name=org_name,
            defaults={
                "type_of_organization": request.POST.get("type_of_organization"),
                "country_of_operation": request.POST.get("country_of_operation"),
                "organization_size": request.POST.get("organization_size") or 0,
                "revenue_size": request.POST.get("revenue_size") or 0,
                "website_url": request.POST.get("website_url"),
                "social_media": request.POST.get("social_media"),
            }
        )

        # Create client
        client = Client.objects.create(
            name=request.POST.get("name"),
            position=request.POST.get("position"),
            email=request.POST.get("email"),
            phone_number=request.POST.get("phone"),
            organization=organization,
        )

        # Add sector and auto-set status
        Sector.objects.create(client=client, sector=request.POST.get("sector"))
        Status.objects.create(client=client, status="Attracted")

        return redirect("https://otabr.pythonanywhere.com/")

    return render(request, "polls/public_form.html")
