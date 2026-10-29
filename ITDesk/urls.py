
from django.urls import path
from .views import (
    fetch_subcategories,
    ticket_list,
    it_ticket_detail,
    export_tickets_excel,
    raise_ticket,
    it_dashboard,
    view_renewals,
    system_info,
    receive_asset_info,
    addvendor,
    vendor_list,
    addinvoice,
    invoice_list,
    deletevendor,
    deleteinvoice,
    add_asset,
    asset_list,
    edit_asset,
    delete_asset,
    add_voip,
    edit_voip,
    list_voip,
    export_voip_excel,
)

app_name = "ITDesk"

urlpatterns = [
    # Tickets
    path("fetch-subcategories/", fetch_subcategories, name="fetch_subcategories"),
    path("it/ticket/<str:ticket_id>/", it_ticket_detail, name="it_ticket_detail"),
    path("tickets/list", ticket_list, name="ticket_list"),
    path("tickets/raise/", raise_ticket, name="raise_ticket"),
    path("tickets/export/", export_tickets_excel, name="export_tickets_excel"),

    # Dashboard and utilities
    path("it_dashboard/", it_dashboard, name="it_dashboard"),
    path("view_renewals/", view_renewals, name="view_renewals"),
    path("system_info/", system_info, name="system_info"),

    # Asset API
    path("api/receive-asset/", receive_asset_info, name="receive_asset_info"),

    # Vendors
    path("vendor/add/", addvendor, name="addvendor"),
    path("vendor/list/", vendor_list, name="vendor_list"),
    path("vendor/delete/<int:pk>/", deletevendor, name="deletevendor"),

    # Invoices
    path("invoice/add/", addinvoice, name="addinvoice"),
    path("invoice/list/", invoice_list, name="invoice_list"),
    path("invoice/delete/<int:pk>/", deleteinvoice, name="deleteinvoice"),

    # Assets
    path("asset/add/", add_asset, name="addasset"),
    path("asset/list/", asset_list, name="assetlist"),
    path("asset/edit/<int:asset_id>/", edit_asset, name="editasset"),
    path("asset/delete/<int:asset_id>/", delete_asset, name="deleteasset"),

    # VoIP
    path("add_voip/", add_voip, name="add_voip"),
    path("voip/edit/<int:pk>/", edit_voip, name="edit_voip"),
    path("list_voip/", list_voip, name="list_voip"),
    path("voip/export/", export_voip_excel, name="export_voip_excel"),
]
