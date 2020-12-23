#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""QT Dropdown Widget."""

import os
# Qt.py from Mottosso
# https://github.com/mottosso/Qt.py
from Qt import QtWidgets

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(WORKING_DIR, 'resources')


class DropdownWidget(QtWidgets.QWidget):
    """Widget designed to work like a dropdown menu."""

    BTN_HEIGHT = 25
    BTN_ICON_SIZE = QtCore.QSize(6, 6)

    ICON_OPEN_ARROW = QtGui.QIcon(os.path.join(RESOURCES_DIR, 'icons', 'icon_arrow_open.png'))
    ICON_CLOSE_ARROW = QtGui.QIcon(os.path.join(RESOURCES_DIR, 'icons', 'icon_arrow_close.png'))

    CSS_BTN = 'QPushButton{background-color: #262626; color: #888888; text-align: left; padding-left: 10px;}' \
              'QPushButton:checked{background-color: #444444; color: #FFFFFF} ' \
              'QPushButton:hover{color: #FFFFFF}'

    def __init__(self, parent=None, text='', isExpanded=True, defaultLayout=QtWidgets.QFormLayout):
        """Initialize DropdownWidget.

        Args:
            parent(QtWidgets.QWidget): Parent Widget, default is None
            text(str): DropDown title, default is ''
            isExpanded(bool): Dropdown is expanded by default. Default is True
            defaultLayout(QtWidget.QLayout): Default layout to use. Default is `QtWidgets.QFormLayout`
        """
        super(DropdownWidget, self).__init__(parent or getKatanaMainWindow())

        if not isinstance(defaultLayout(), QtWidgets.QLayout):
            raise AttributeError('QtWidgets.QLayout expected but got', type(defaultLayout))

        self.__isExpanded = bool(isExpanded)

        self._btnDropdown = QtWidgets.QPushButton()
        self._containerDropDown = QtWidgets.QWidget()

        self._lytRoot = QtWidgets.QVBoxLayout(self)
        self._lytContainer = defaultLayout(self._containerDropDown)

        self._lytRoot.addWidget(self._btnDropdown)
        self._lytRoot.addWidget(self._containerDropDown)

        self.setText(text)
        self.setExpand(self.__isExpanded)

        # Setup UI
        self._btnDropdown.setCheckable(True)
        self._btnDropdown.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self._btnDropdown.setFixedHeight(self.BTN_HEIGHT)
        self._btnDropdown.setFlat(True)
        self._btnDropdown.setIconSize(self.BTN_ICON_SIZE)
        self._btnDropdown.setStyleSheet(self.CSS_BTN)

        # Signals
        self._btnDropdown.clicked.connect(self.toggleCollapse)

    def addWidget(self, widget):
        """Add Widget to the container.
        If you use a QGridLayout, please use `self.layout()`

        Args:
            widget(QtWidgets.QWidget): Widget to add
        """
        self._lytContainer.addWidget(widget)

    def addWidgets(self, *widgets):
        """Add Widgets to the container.
        If you use a QGridLayout, please use `self.layout()`

        Args:
            widgets(list(QtWidgets.QWidget)): Widgets to add
        """
        map(self._lytContainer.addWidget, widgets)

    def addRow(self, label, widget):
        """Add Row to the container.

        Args:
            label(QtWidgets.QLabel): label text
            widget(QtWidgets.QWidget): Widget to add
        """
        if not isinstance(self._lytContainer, QtWidgets.QFormLayout):
            raise RuntimeError('This method is only used for QtWidgets.QFormLayout', type(self._lytContainer))

        self._lytContainer.addRow(label, widget)

    def addRows(self, *rows):
        """Add Widgets to the container.
        If you use a QGridLayout, please use `self.layout()`

        Args:
            rows(list(tuple(QtWidgets.QWidget, QtWidgets.QWidget))): Widgets to add
        """
        for row in rows:
            label, widget = row
            self.addRow(label, widget)

    def layout(self):
        """Get container's layout.

        Returns:
            (QtWidgets.QLayout): Container's layout.
        """
        return self._lytContainer

    def setLayout(self, layout):
        """Set layout for the container.

        Args:
            layout(QtWidgets.QLayout): Set new layout
        """
        self._containerDropDown.setLayout(layout)

    def setText(self, text):
        """Set title dropdown.

        Args:
            text(str): Dropdown title
        """
        self._btnDropdown.setText(' {}'.format(text))

    def expand(self):
        """Expand the Dropdown."""
        self.setExpand(True)

    def collapse(self):
        """Collapse the Dropdown."""
        self.setCollapse(True)

    def setCollapse(self, value):
        """Set if the dropdown does collapse.

        Args:
            value(bool): The dropdown does collapse
        """
        self.__isExpanded = value
        self.toggleCollapse()

    def setExpand(self, value):
        """Set if the Dropdown does expand.

        Args:
            value(bool): The Dropdown does expand
        """
        self.__isExpanded = not value
        self.toggleCollapse()

    def toggleCollapse(self):
        """Toggle either expand or collapse dropdown."""
        self.__isExpanded = not self.__isExpanded

        self._btnDropdown.setChecked(self.__isExpanded)
        self._btnDropdown.setIcon(self.ICON_OPEN_ARROW if self.__isExpanded else self.ICON_CLOSE_ARROW)
        self._containerDropDown.setVisible(self.__isExpanded)

    def isExpanded(self):
        """Does the Dropdown is expanded.

        Returns:
            (bool): Does the Dropdown is expanded
        """
        return self.__isExpanded

    def isCollapsed(self):
        """Does the Dropdown is collapsed.

        Returns:
            (bool): Does the Dropdown is collapsed
        """
        return not self.__isExpanded
