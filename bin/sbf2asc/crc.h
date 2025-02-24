/*
 * crc.h: Declaration of functions to compute and validate
 *        a CRC.
 *
 * Septentrio grants permission to use, copy, modify, and/or distribute
 * this software for any purpose with or without fee.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND SEPTENTRIO DISCLAIMS ALL
 * WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
 * SEPTENTRIO BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
 * CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
 * OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
 * NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
 * CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

#ifndef CRC_H
#define CRC_H 1

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/*---------------------------------------------------------------------------*/
/* This function computes the CRC of a buffer "buf" of "buf_length" bytes. */

uint16_t CRC_compute16CCITT(const void* buf, size_t buf_length);

/*---------------------------------------------------------------------------*/
/* This function computes the CRC of a buffer "buf" of "buf_length" bytes and an initial "crc" value. */

uint16_t CRC_compute16CCITTCompute(const void* buf, size_t buf_length, uint16_t crc);

/*---------------------------------------------------------------------------*/
/* Returns true if the CRC check of the SBFBlock is passed. */

bool CRCIsValid(const void* Mess);

#ifdef __cplusplus
}
#endif

#endif
