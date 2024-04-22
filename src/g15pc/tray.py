import logging
import gi
from g15pc.ipc import client
from g15pc.acpi import calls
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator  # noqa: E402

LOG = logging.getLogger('generic')


class Menu(gtk.Menu):

    def __init__(self):
        super().__init__()

        self.active_power_mode = None
        self.power_mode_item_dict = {}
        self.toggle_g_mode_item = self.create_gameshift_button()
        self.power_mode_sub_menu, self.power_mode_item = self.create_power_mode_submenu()

        self.append(self.toggle_g_mode_item)
        self.append(self.power_mode_item)
        self.append(gtk.SeparatorMenuItem())
        self.append(self.create_tray_exit_button())

        self.show_all()

    def create_gameshift_button(self) -> gtk.MenuItem:
        LOG.debug('Creating Gameshift button')
        toggle_g_mode_item = gtk.MenuItem(label='Toggle Gameshift')
        toggle_g_mode_item.connect('activate', self.handle_action, 'toggle_G_mode', None)
        return toggle_g_mode_item

    def create_power_mode_submenu(self) -> gtk.Menu:
        LOG.debug('Creating power mode menu')
        power_mode_sub_menu = gtk.Menu()
        power_mode_sub_menu.connect('show', self.on_popup)
        group = None
        for pmitem in calls.PowerModes:
            power_mode = weird_case(pmitem.name)
            item = gtk.RadioMenuItem(group=group, label=power_mode)
            # item.set_active(selected_power_mode == power_mode)
            func = item.connect('activate', self.handle_action, 'set_power_mode', power_mode)
            if group is None:
                group = item
            power_mode_sub_menu.append(item)
            self.power_mode_item_dict[power_mode] = (item, func)

        power_mode_item = gtk.MenuItem(label='Set power mode')
        power_mode_item.set_submenu(power_mode_sub_menu)

        return power_mode_sub_menu, power_mode_item

    def create_tray_exit_button(self) -> gtk.MenuItem:
        exittray = gtk.MenuItem(label='Exit Tray')
        exittray.connect('activate', self.exit_tray)
        return exittray

    def handle_action(self, _, req, arg=None):
        LOG.debug('Request: %s %s', req, arg)
        command = client.MESSAGE_TYPES.get(req)
        if command is None:
            LOG.error('Invalid request: %s', req)
            return

        res = command(arg)
        LOG.debug('Response: %s', res)

    def exit_tray(self, _):
        gtk.main_quit()

    def on_popup(self, _):
        '''
        Update selected power mode on submenu popup
        '''
        LOG.debug('Updating power mode menu...')
        power_mode = client.get_power_mode(None)
        item, handler = self.power_mode_item_dict[weird_case(power_mode)]

        # find previous selected item
        child = None
        LOG.debug('Locating previous power mode item...')
        for child in self.power_mode_sub_menu.get_children():
            if isinstance(child, gtk.RadioMenuItem) and child.get_active():
                break

        previous_power_mode = child.get_label()
        old_item, old_handler = self.power_mode_item_dict[previous_power_mode]
        LOG.debug('Previous power mode: %s', previous_power_mode)

        old_item.handler_block(old_handler)
        item.handler_block(handler)
        item.set_active(True)
        item.handler_unblock(handler)
        old_item.handler_unblock(old_handler)
        LOG.debug('Active power mode: %s', power_mode)


# Converts string to WEIRD_Case
def weird_case(string):
    pos = string.find('_') + 1
    return string[:pos] + string[pos:].capitalize()


def create_indicator():
    indicator = appindicator.Indicator.new(
        "customtray",
        "alien_grey",
        appindicator.IndicatorCategory.APPLICATION_STATUS
    )

    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    menu = Menu()
    indicator.set_menu(menu)
    gtk.main()


if __name__ == "__main__":
    create_indicator()
