/*
 * sbfsigtypes.h: Definition of GNSS signal types used by Septentrio receivers.
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
/**
 *  \file
 *  \ingroup sbfdata
 *  \brief Declaration of an enumeration for satellite signals.
 *
 *  Declaration and definition of an enumeration for satellite signals.
 *
 *  \par Copyright:
 *    (c) 2000-2015 Copyright Septentrio NV/SA. All rights reserved.
 */

#ifndef SBFSIGTYPES_H
#define SBFSIGTYPES_H 1               /* To avoid multiple inclusions */


/**
 * \brief Enumeration of the different signal modulations.
 * It is important not to mix signal types from different constellations.
 */
typedef enum
{
    SIG_GPSL1CA = 0,  /**< GPS L1 C/A        */
    SIG_GPSL1P  = 1,  /**< GPS L1 P(Y)       */
    SIG_GPSL2P  = 2,  /**< GPS L2 P(Y)       */
    SIG_GPSL2C  = 3,  /**< GPS L2C           */
    SIG_GPSL5   = 4,  /**< GPS L5            */
    SIG_GPSL1C  = 5,  /**< GPS L1C           */
    SIG_QZSL1CA = 6,  /**< QZSS L1 C/A       */
    SIG_QZSL2C  = 7,  /**< QZSS L2C          */
    SIG_GLOL1CA = 8,  /**< GLONASS L1 C/A    */
    SIG_GLOL1P  = 9,  /**< GLONASS L1 P      */
    SIG_GLOL2P  = 10, /**< GLONASS L2 P      */
    SIG_GLOL2CA = 11, /**< GLONASS L2 C/A    */
    SIG_GLOL3   = 12, /**< GLONASS L3        */
    SIG_BDSB1C  = 13, /**< BeiDou B1C        */
    SIG_BDSB2a  = 14, /**< BeiDou B2a        */
    SIG_IRNL5   = 15, /**< IRNSS L5          */
    SIG_RES16_  = 16, /**< Reserved -- do not use */
    SIG_GALE1BC = 17, /**< Galileo E1 BC     */
    /**< Reserved                            */
    SIG_GALE6BC = 19, /**< Galileo E6 BC     */
    SIG_GALE5a  = 20, /**< Galileo E5a       */
    SIG_GALE5b  = 21, /**< Galileo E5b       */
    SIG_GALE5   = 22, /**< Galileo E5 AltBOC */
    SIG_MSS     = 23, /**< MSS L-Band signal */
    SIG_SBSL1CA = 24, /**< SBAS L1 C/A       */
    SIG_SBSL5   = 25, /**< SBAS L5           */
    SIG_QZSL5   = 26, /**< QZSS L5           */
    SIG_QZSL6   = 27, /**< QZSS L6           */
    SIG_BDSB1I  = 28, /**< BeiDou B1I        */
    SIG_BDSB2I  = 29, /**< BeiDou B2I        */
    SIG_BDSB3   = 30, /**< BeiDou B3         */
    SIG_UNUSED  = 31, /**<                   */
    SIG_QZSL1C  = 32, /**< QZSS L1C          */
    SIG_QZSL1S  = 33, /**< QZSS L1S          */
    SIG_BDSB2b  = 34, /**< BeiDou B2b        */
    /**< reserved                            */
    SIG_IRNS1   = 36, /**< IRNSS S-band - Tentative.  Do not use yet! */
    SIG_IRNL1   = 37, /**< IRNSS L1 */
    SIG_QZSL1CB = 38, /**< QZSS L1C/B   - Tentative.  Do not use yet! */
    SIG_QZSL5S  = 39, /**< QZSS L5S          */
    SIG_LAST    = 40, /**< (This must be the last item in the list, never delete it.) */
    SIG_INVALID = 255
} SignalType_t;


/* old signal names */
#define L1CA       SIG_GPSL1CA
#define L1P        SIG_GPSL1P
#define L2P        SIG_GPSL2P
#define L2C        SIG_GPSL2C
#define L5         SIG_GPSL5
#define L1CAQZS    SIG_QZSL1CA
#define L2CQZS     SIG_QZSL2C
#define L1CAGLO    SIG_GLOL1CA
#define L1PGLO     SIG_GLOL1P
#define L2PGLO     SIG_GLOL2P
#define L2CAGLO    SIG_GLOL2CA
#define L3GLO      SIG_GLOL3
#define L5IRNSS    SIG_IRNL5
#define L1BC       SIG_GALE1BC
#define E6BC       SIG_GALE6BC
#define E5a        SIG_GALE5a
#define E5b        SIG_GALE5b
#define E5         SIG_GALE5
#define MSS_LBAND  SIG_MSS
#define L1GEO      SIG_SBSL1CA
#define L5GEO      SIG_SBSL5
#define L5QZS      SIG_QZSL5
#define L6QZS      SIG_QZSL6
#define E2CMP      SIG_BDSB1I
#define E5bCMP     SIG_BDSB2I
#define B3CMP      SIG_BDSB3


#endif
/* End of "ifndef SBFSIGTYPES_H" */
