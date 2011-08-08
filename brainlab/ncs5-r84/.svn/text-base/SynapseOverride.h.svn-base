/*
 *  SynapseOverride.h
 *  ncs5
 *
 *  Created by James King on 5/27/07.
 *  Copyright 2007 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef SYNAPSEOVERRIDE_H
#define SYNAPSEOVERRIDE_H

//For some reason, mpi must be included (via this Global header) first.
#include "Global.h"
#include "InitStruct.h"
#include <vector>

using namespace std;

class SynapseDef;
class Synapse;
class CellManager;
class Brain;

/**
 * The SynapseOverride is an event which can occur during the simulation to override the
 * USE value for a synapse to one printed in a text file supplied by the user.
 */
class SynapseOverride
{
    private:
        /**
         * Reference to synapses which need their USE values altered
         */
        vector<Synapse *> synapseAccess;
        
        /**
         * The USE values which will be put into place when the time comes
         */
        vector<double> replacementUSE;
                
        /**
         * When the override will take place
         */
        double time;
        
        /**
         * File with the override values.  There is a header on the first line that will be used to
         * validate that the file contains the right amount of values to correspond with the number
         * of synapses that exist.  The second line will contain the actual USE values.
         */
        char *file;
        
    public:
        /**
         * Constructor
         */
        SynapseOverride( T_EVENT *pEvent, CellManager *pCellManager, Brain *brain );
        
        /**
         * Test whether this SynapseOverride affects any cells/synapses
         */
        bool empty() const;
        
        /**
         * Less than operator to allow priority_queue maintenence.  Looks at
         * double time to give lowest times higher priority
         */
        bool operator<( const SynapseOverride &RHS ) const;
        
        /**
         * Get the time when this override should be applied
         *
         * @return Time of override application
         */
        double getTime() const;
        
        /**
         * When the time has come for the override to take place, whoever was monitoring (Brain.cpp in DoThink loop)
         * will invoke this function.   Note that this function is const because the priority queue needs to
         * know that any objects stored in it won't make any modifications that could affect order.  Since
         * executing the USE override will not affect the timing, it is okay.
         */
        void execute() const;

};

//----------------------------------------------------------------------------------
// Inline functions
//----------------------------------------------------------------------------------

inline bool SynapseOverride::operator<( const SynapseOverride &RHS ) const
{
    //this is using greater than on purpose.  It flips the priority queue's behavior
    return time > RHS.time;
}

//----------------------------------------------------------------------------------

inline double SynapseOverride::getTime() const
{
    return time;
}

//----------------------------------------------------------------------------------

inline bool SynapseOverride::empty() const
{
    return synapseAccess.empty();
}

#endif
