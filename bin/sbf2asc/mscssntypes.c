/*!
\impl_public
  \defgroup mscssntypes_impl_windows ssntime windows implementation
  This implementation fixes the fact that the snprintf function in MSVC does not add a trailing '\0' when
  the given string is equal or larger than the given buffer.
  \ingroup ssntypes
*/
/*!
\impl_private
  \file
  \brief Definitions of the function declared in "mscssntypes.h".
  \ingroup ssntime_impl_windows

  This implementation fixes the fact that the snprintf function in MSVC does not add a trailing '\0' when
  the given string is equal or larger than the given buffer.

  \par Origin:
  General

  \par Author:
    Kristof Van Wassenhove
  \par Backup:


  \par Copyright:
  (c) 2008 Septentrio Satellite Navigation nv/sa, Belgium

*/
#if (_MSC_VER < 1800)
#include <stdarg.h>
#include <stdio.h>

#include "mscssntypes.h"

int slprintf(char* buffer, size_t count, const char* fmt, ...)
{
    va_list ap;
    int ret;

    va_start(ap, fmt);
    ret = _vsnprintf(buffer, count - 1, fmt, ap);
    buffer[count - 1] = '\0';

    if (ret < 0)
    {
        ret = (int) count;
    }

    va_end(ap);
    return ret;
}
#endif

/* END OF FILE ==============================================================*/
/*!
\end_impl_private
\end_impl_public
*/
