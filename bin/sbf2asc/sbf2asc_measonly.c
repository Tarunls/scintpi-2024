/*
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

/* This file shows how to build a mini application using the C
   functions in sbfread.c and sbfread_meas.c to decode the
   measurement-related SBF blocks (MeasEpoch, Meas3Ranges, etc).

   The application expects the name of a SBF file as only
   argument. For each measurement epoch in the file, it prints the
   epoch time, the list of satellites, and the L1/E1/B1 pseudorange.
*/

#include "sbfread.h"

void main(int argc, char* argv[])
{
    SBFData_t   SBFData;
    uint8_t     SBFBlock[MAX_SBFSIZE];
    MeasEpoch_t MeasEpoch;

    /* initialize the data containers that will be used to decode the SBF blocks */
    InitializeSBFDecoding(argv[1], &SBFData);

    /* read all SBF blocks from the file, one by one */
    while (GetNextBlock(&SBFData, SBFBlock, BLOCKNUMBER_ALL, BLOCKNUMBER_ALL,
                        START_POS_CURRENT | END_POS_AFTER_BLOCK) == 0)
    {
        /* SBFBlock contains an SBF block as read from the file.  All
           blocks are sent to sbfread_MeasCollectAndDecode().  The
           function collects measurement-related blocks (MeasEpoch,
           MeasExtra, Meas3Ranges, Meas3Doppler, etc...), and returns true
           when a complete measurement epoch is available.  The decoded
           measurement epoch containing all observables from all
           satellites is provided in the MeasEpoch structure. */
        if (sbfread_MeasCollectAndDecode(&SBFData, SBFBlock, &MeasEpoch, SBFREAD_ALLMEAS_ENABLED))
        {
            int i;

            /* In this example, we print the epoch time in millisecond and the list
               of the satellites for which measurements are available (PRN
               numbering defined in sviddef.h).  For GPS, GLONASS, Galileo
               and BDS satellites, the L1/E1/B1 pseudorange is printed as well. */
            printf("TOW:%d\n", (int)MeasEpoch.TOW_ms);

            /* go through all satellites */
            for (i = 0; i < MeasEpoch.nbrElements; i++)
            {
                uint32_t SigIdx;

                /* print the satellite number (as per sviddef.h) */
                printf("%3d ", MeasEpoch.channelData[i].PRN);

                /* look for the measurement set containing L1CA, E1BC or
                   BDSB1I observables */
                for (SigIdx = 0; SigIdx < MAX_NR_OF_SIGNALS_PER_SATELLITE; SigIdx++)
                {
                    const MeasSet_t* const MeasSet = &(MeasEpoch.channelData[i].measSet[0][SigIdx]);

                    if (MeasSet->flags != 0)
                    {
                        SignalType_t SignalType = (SignalType_t)MeasSet->signalType;

                        if (SignalType == SIG_GPSL1CA || SignalType == SIG_GLOL1CA || SignalType == SIG_GALE1BC || SignalType == SIG_BDSB1I)
                        {
                            printf("(%.3f) ", MeasSet->PR_m);
                        }
                    }
                }

                printf("\n");
            }
        }
    }
}
