//
// Created by pkleczek on 9/30/20.
//

#ifndef IMPLEMENTATION_INFINITY_HPP
#define IMPLEMENTATION_INFINITY_HPP

#include <limits>
#include <vector>

/// The data type used to represent costs in the cost matrix.
using cost_t = int;

/// A cost representing a forbidden transition.
const cost_t INF = std::numeric_limits<cost_t>::max();

/// Test if a cost represents a forbidden transition.
bool is_inf(cost_t val);

/// Represents a path (i.e., a sequence of vertices' indexes).
using path_t = std::vector<std::size_t>;

/**
 * The <tt>StageState</tt> class stores information about the partial solution
 * at the given stage.
 */
class IStageState {
public:
    virtual path_t get_path() = 0;
    virtual std::size_t get_level() const = 0;
    virtual cost_t get_lower_bound() const = 0;
};

#endif //IMPLEMENTATION_INFINITY_HPP
