# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard.api import keystone
from openstack_dashboard.api import nova
from openstack_dashboard.usage import quotas

from openstack_dashboard.dashboards.admin.info.tables import NovaServicesTable
from openstack_dashboard.dashboards.admin.info.tables import QuotasTable
from openstack_dashboard.dashboards.admin.info.tables import ServicesTable


class DefaultQuotasTab(tabs.TableTab):
    table_classes = (QuotasTable,)
    name = _("Default Quotas")
    slug = "quotas"
    template_name = ("horizon/common/_detail_table.html")

    def get_quotas_data(self):
        request = self.tab_group.request
        try:
            quota_set = quotas.get_default_quota_data(request)
            data = quota_set.items
        except:
            data = []
            exceptions.handle(self.request, _('Unable to get quota info.'))
        return data


class ServicesTab(tabs.TableTab):
    table_classes = (ServicesTable,)
    name = _("Services")
    slug = "services"
    template_name = ("horizon/common/_detail_table.html")

    def get_services_data(self):
        request = self.tab_group.request
        services = []
        for i, service in enumerate(request.user.service_catalog):
            service['id'] = i
            services.append(
                keystone.Service(service, request.user.services_region))
        return services


class NovaServicesTab(tabs.TableTab):
    table_classes = (NovaServicesTable,)
    name = _("Compute Services")
    slug = "nova_services"
    template_name = ("horizon/common/_detail_table.html")

    def get_nova_services_data(self):
        try:
            services = nova.service_list(self.tab_group.request)
        except Exception:
            services = []
            msg = _('Unable to get nova services list.')
            exceptions.check_message(["Connection", "refused"], msg)
            raise

        return services


class SystemInfoTabs(tabs.TabGroup):
    slug = "system_info"
    tabs = (ServicesTab, NovaServicesTab, DefaultQuotasTab,)
    sticky = True
