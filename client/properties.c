/*
 *
 *  Wireless daemon for Linux
 *
 *  Copyright (C) 2018  Intel Corporation. All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License as published by the Free Software Foundation; either
 *  version 2.1 of the License, or (at your option) any later version.
 *
 *  This library is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public
 *  License along with this library; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <ell/ell.h>

#include "properties.h"

bool properties_parse_args(char *args, char **name, char **value)
{
	char **arg_arr;

	if (!args)
		return false;

	arg_arr = l_strsplit(args, ' ');

	if (!arg_arr || !arg_arr[0] || !arg_arr[1]) {
		l_strfreev(arg_arr);
		return false;
	}

	*name = l_strdup(arg_arr[0]);
	*value = l_strdup(arg_arr[1]);

	l_strfreev(arg_arr);

	return true;
}